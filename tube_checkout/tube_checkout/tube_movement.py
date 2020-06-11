import asyncio
from . import hid
import concurrent.futures
import re
import subprocess
import time
import json
import os.path
from opentrons import types
from opentrons.types import Point as p
from opentrons.hardware_control.types import Axis
from opentrons.drivers.smoothie_drivers.driver_3_0 import SmoothieError
offset_file = '/data/grabber_calibration_new.json'

import pkgutil

json_24rack = pkgutil.get_data(__name__, 'labware/24_2ml_rack.json').decode()
custom_rack = json.loads(json_24rack)

class TubeMover():
    grab_extra = p(0, -1, 0)  # grab slightly off-center to ensure grip
    drop_with_low_current = True
    home_after_drop = True
    rotate_dist = 15
    neg_rotate_dist = -16
    start_rotate_x = 310
    roll_height = 78
    roll_y = 218
    scan_x_start = 395
    scan_x_end = 410
    grab_speed = 40
    dropping_speed = 70
    old_barcode = None
    # we want the tool to be just above the rack
    tube_offset = p(0, 0, 2.5)
    tweak = types.Point(0, 0, 0)
    drop_with_shake=False
    block_consecutive_barcodes = True

    def __init__(self, protocol, mount=types.Mount.RIGHT, low_drop_current=0.1, use_transit_channel=False):
        if mount != types.Mount.RIGHT and mount != "right":
            raise ValueError("Only right mount supported for now.")
        self.protocol = protocol
        self.mount = mount
        self.establish_positions()
        # This current (in amps) is used for the Z stepper when dropping tubes to minimise the damage caused by any collision due to misaligned tubes.
        self.low_drop_current = low_drop_current
        self.use_transit_channel = use_transit_channel
        #protocol.delay(seconds=0.1)

    def get_current_pos(self):
        return self.protocol._hw_manager.hardware.gantry_position(self.mount)

    def read_offsets_file(self):

        try:
            with open(offset_file) as json_file:
                offsets = json.load(json_file)
        except FileNotFoundError:
            offsets = {'x': 0, 'y': 0, 'z': 0}
        return offsets

    def update_offsets_file(self, key, value):
        """ Set one coordinate of the offsets file. """
        int_offsets = self.read_offsets_file()
        int_offsets[key] = value
        with open(offset_file, 'w') as outfile:
            json.dump(int_offsets, outfile)

    def get_rack(self, position):
        """ Load a custom 24 ml tube rack onto the deck and return it."""
        return self.protocol.load_labware_from_definition(
            custom_rack,
            position,
            "2ml_rack",
        )

    def fast_home_checking_for_issues(self, margin):
        """ Homes the Z axis in such a way that it if it has skipped steps an error will result. 

        This is to detect crashes and stop."""
        if self.protocol.is_simulating():
            return
        cur_pos = self.get_current_pos()
        deck_bounds = self.protocol._hw_manager.hardware._deck_from_smoothie(
            {'X': cur_pos.x, 'Y': cur_pos.y, 'Z': self.protocol._hw_manager.hardware._backend.axis_bounds['A'][1], 'A': self.protocol._hw_manager.hardware._backend.axis_bounds['A'][1]})

        max_z = deck_bounds[Axis.A]
        try:
            self.move_z(max_z-margin, speed=500)
            # slow down in case we hit the endstop
            self.move_z(max_z, speed=60)
        except SmoothieError():
            raise SmoothieError(
                "It looks like there was a collision. Robot is stopping to prevent damage.")
        self.protocol._hw_manager.hardware.home_z(types.Mount.RIGHT)

    def establish_positions(self):
        # TODO refactor most of this into class vars at top
        initial_offsets = self.read_offsets_file()
        initial_offsets = p(
            initial_offsets['x'], initial_offsets['y'], initial_offsets['z'])
        self.offset = initial_offsets + self.tweak

        self.safe_y_not_offset = 250
        self.safe_y_with_offset = 250 + self.offset.y
        self.grabbing_move = p(0, -13, 0)
        self.hold_up_offset = p(0, 0, 80)
        self.jerk_up_offset = p(0, 0, 40)
        self.just_before_offset = p(0, 0, 40)
        self.brief_down_offset = p(0, 0, -20)
        little_move = 2.5
        self.move1 = p(little_move, 0, 0)
        self.move2 = p(0, little_move, 0)
        self.move3 = p(-little_move, 0, 0)
        self.move4 = p(0, -little_move, 0)
        self.down_offset = p(0, 0, -10)
        self.hover_height1 = 84+self.offset.z
        self.hover_height2 = 82+self.offset.z
        self.hover_height3 = 80+self.offset.z

    def move(self, position, speed=None):
        if self.protocol.is_simulating():
            return
        self.set_movement_acceleration()
        self.protocol._hw_manager.hardware.move_to(
            types.Mount.RIGHT, position, speed=speed)

    def move_to_attachment_position(self):
        self.move(p(200, 40, 210))
        self.move(p(200, 40, 30))

    def move_x(self, x, speed=None):
        cur_point = self.get_current_pos()
        new_point = p(x, cur_point.y, cur_point.z)
        self.move(new_point, speed=speed)

    def move_y(self, y, speed=None):
        cur_point = self.get_current_pos()
        new_point = p(cur_point.x, y, cur_point.z)
        self.move(new_point, speed=speed)

    def move_z(self, z, speed=None):
        cur_point = self.get_current_pos()
        new_point = p(cur_point.x, cur_point.y, z)
        self.move(new_point, speed=speed)

    def move_to_transit_channel(self):
        self.move_y(self.safe_y_with_offset)

    def move_via_transit_channel(self, point):
        """Move via a particular y channel."""
        higher_z = max(self.get_current_pos().z, point.z)
        # self.move_z(higher_z)
        self.move_y(self.safe_y_with_offset)
        # self.move_x(point.x)
        self.move(p(point.x, self.safe_y_with_offset, higher_z))
        self.move_y(point.y)
        self.move_z(point.z)

    def rotate_tube(self, negative=False):
        """Rotate the tube using the rubber band."""
        rotate_dist = self.rotate_dist
        start_rotate_x = self.start_rotate_x+self.offset.x
        if negative == True:
            start_rotate_x = start_rotate_x + 20
            rotate_dist = rotate_dist = self.neg_rotate_dist
        roll_y = self.roll_y + self.offset.y
        roll_height = self.roll_height+self.offset.z

        self.move_via_transit_channel(
            p(start_rotate_x, self.safe_y_with_offset, roll_height+2))
        self.move(p(start_rotate_x, roll_y, roll_height+2), speed=150)
        self.move(p(start_rotate_x, roll_y, roll_height), speed=150)
        self.move(p(start_rotate_x+rotate_dist,
                    roll_y, roll_height), speed=150)
        self.move(p(start_rotate_x+rotate_dist,
                    self.safe_y_with_offset, roll_height), speed=150)

    def scan_barcode(self, if_fails="raise_error", num_to_give_up=7):
        """Scan the barcode of the current tube."""
        self.protocol.comment("Attempting to scan barcode" )
        if self.protocol.is_simulating():
            return "123456"
        scanning_speed = 10
        scanning_y = 240+self.offset.y
        scanning_height = 80 + self.offset.z
        x_start = self.scan_x_start + self.offset.x
        x_end = self.scan_x_end + self.offset.x

        presentation_position = p(200, 20, 200) + self.offset

        if self.use_transit_channel:
            self.move_via_transit_channel(
                p(x_start, scanning_y, scanning_height))
        else:
            cur_pos = self.get_current_pos()
            self.move(p(x_start, scanning_y, max(cur_pos.z, scanning_height)))
            self.move(p(x_start, scanning_y, scanning_height))
        executor = concurrent.futures.ThreadPoolExecutor()
        future = executor.submit(hid.get_barcode)
        self.move(p(x_end, scanning_y, scanning_height), speed=scanning_speed)
        try:
            return_value = future.result(timeout=0.2)
            if return_value == self.old_barcode and self.block_consecutive_barcodes and not self.protocol.is_simulating():
                raise ValueError("Got the same barcode twice in a row, this can indicate a collision. If you need to be able to scan the same barcode twice in a row, disable block_consecutive_barcodes.")
            self.old_barcode = return_value
            return return_value
        except (asyncio.TimeoutError, FileNotFoundError) as e:
            if type(e) == FileNotFoundError:
                raise ValueError(
                    "Could not detect barcode scanner - is it connected and in HID mode?")
                num_to_give_up = num_to_give_up + 1
            if num_to_give_up > 0:
                negative = num_to_give_up > 3
                self.rotate_tube(negative=negative)
                return self.scan_barcode(num_to_give_up=num_to_give_up-1)
            else:
                if if_fails == "raise_error":
                    raise ValueError(
                        "Unable to find barcode for this tube, you can change how to respond to this by modifying the if_fails parameter.")
                elif if_fails == "prompt_for_barcode":
                    self.move_via_transit_channel(presentation_position)
                    barcode_input = ""
                    while not len(barcode_input) > 5:
                        barcode_input = input(
                            "Please manually scan the barcode")
                    return barcode_input
                elif if_fails == "manually_scan":
                    executor = concurrent.futures.ThreadPoolExecutor()
                    future = executor.submit(hid.get_barcode)
                    self.move_via_transit_channel(presentation_position)
                    protocol.pause(
                        "Could not scan barcode. Please remove the tube from the holder, manually scan it with the scanner inside the robot, then replace it on the holder and resume the protocol.")
                elif if_fails == "return_false":
                    return False

    def get_position_for(self, tube):
        """Gets the movement position for a tube."""
        rack_position = tube.top().point
        new_pos = rack_position + self.offset
        
        new_pos = new_pos + self.tube_offset
        return new_pos

    def ensure_z_is_above(self, z):
        """Move to height z or above."""
        current_pos = self.get_current_pos()
        if current_pos.z < z:
            self.move_z(z)


    def grab(self, tube):
        """Grab a tube from position specified by tube."""

        self.protocol.comment("Grabbing tube from {}".format(tube) )

        key_pos = self.get_position_for(tube)
        self.ensure_z_is_above(
            (key_pos - self.grabbing_move + self.hold_up_offset).z)

        if self.use_transit_channel:
            self.move_via_transit_channel(
                key_pos - self.grabbing_move)
        else:
            self.move(
                key_pos - self.grabbing_move+self.hold_up_offset)
            self.move(
                key_pos - self.grabbing_move)
        self.move(key_pos+self.grab_extra, speed=self.grab_speed)
        self.move(key_pos+self.hold_up_offset)

    def set_movement_acceleration(self):
        """Set acceleration to standard values."""
        if not self.protocol.is_simulating():
            self.protocol._hw_manager.hardware._backend._smoothie_driver.set_acceleration({
            "X": 2000, "Y": 1000, "Z": 1500})

    def set_drop_acceleration(self):
        """Set acceleration to a lower value for dropping."""
        if not self.protocol.is_simulating():
            self.protocol._hw_manager.hardware._backend._smoothie_driver.set_acceleration({
            "Z": 500})

    def set_z_current(self, current):
        """Set the Z active current to a value in amperes to apply less or more force."""
        if self.protocol.is_simulating():
            return
        assert current <= 0.8
        if self.mount == types.Mount.RIGHT:
            axis = Axis.A
        else:
            raise ValueError()
        self.protocol._hw_manager.hardware._backend.set_active_current(
            axis, current)

    def hover_shake(self, key_pos, height):
        """Shake tube to find center of current well."""
        # self.protocol._hw_manager.hardware._backend._smoothie_driver.set_acceleration({
        #                                                                   "X": 200, "Y": 200})
        self.move(p(key_pos.x, key_pos.y, height), speed=60)
        self.move(p(key_pos.x, key_pos.y, height)+self.move1, speed=125)
        self.move(p(key_pos.x, key_pos.y, height)+self.move2, speed=125)
        self.move(p(key_pos.x, key_pos.y, height)+self.move3, speed=125)
        self.move(p(key_pos.x, key_pos.y, height)+self.move4, speed=125)
        self.move(p(key_pos.x, key_pos.y, height), speed=60)

    def drop(self, tube):
        """Drop current tube in the position specified by tube."""
        self.protocol.comment("Dropping tube at {}".format(tube) )
        key_pos = self.get_position_for(tube)
        self.ensure_z_is_above(
            (key_pos - self.grabbing_move + self.hold_up_offset).z)

        if self.use_transit_channel:
            self.move_via_transit_channel(key_pos+self.hold_up_offset)
        else:
            self.move(key_pos+self.hold_up_offset)
        if self.drop_with_shake:
            self.hover_shake(key_pos, self.hover_height2)
            self.hover_shake(key_pos, self.hover_height3)
        else:
            self.move(key_pos+self.just_before_offset)
        # minimise disaster from crash)
        if self.drop_with_low_current:
            self.set_z_current(self.low_drop_current)
        self.set_drop_acceleration()
        self.move(key_pos, speed=self.dropping_speed)
        self.set_movement_acceleration()
        if self.drop_with_low_current:
            self.set_z_current(0.8)
        self.move(key_pos - self.grabbing_move, speed=self.grab_speed)

        if self.home_after_drop:
            self.fast_home_checking_for_issues(60)
        else:
            self.move(key_pos - self.grabbing_move+self.hold_up_offset)