import urwid
import tube_checkout
import time
movement_distances = {"1": 0.1,"2": 0.5, "3":1, "4":5,"5": 10,"6": 20,"7": 50, "8":100};
movement_distance = None

import tube_checkout.utils, tube_checkout.tube_movement
tube_checkout.utils.temporarily_kill_ot_server()
import opentrons.execute
import logging
logging.disable(logging.ERROR)
protocol = opentrons.execute.get_protocol_api('2.2')
protocol._hw_manager.hardware.set_lights(rails=True)
print("Homing... ")
protocol.home()
#protocol._hw_manager.hardware._backend._smoothie_driver.set_acceleration({"X": 100, "Y": 100})
tube_checkout.utils.set_button_as_kill_switch(protocol)

tube_mover = tube_checkout.tube_movement.TubeMover(protocol)
rack = tube_mover.get_rack('5')


from opentrons import types


tube_mover.move( types.Point(135,187,194)) # save user some time by getting to roughly right place


def set_movement_distance(distance):
    global movement_distance
    movement_distance = distance
    movement_distance_txt.set_text(("reverse","Movement distance: {} mm".format(distance)))
 

                
def update_pos():
    pos = tube_mover.get_current_pos()
    pos_txt.set_text(("reverse","Current position: X: {} Y: {} Z: {} ".format(round(pos.x,2),round(pos.y,2),round(pos.z,2)) ))
    
def move_in_direction(direction):
    pos = tube_mover.get_current_pos()
    if movement_distance == "slot":
        if abs(direction.x)>0:
            the_offset = types.Point(direction.x*132.5, 0, 0)
        elif abs(direction.y)>0:
            the_offset =  types.Point(0, direction.y*90.5, 0)
        else:
            the_offset = types.Point(0,0,0)
    else:
        the_offset = types.Point(direction.x*movement_distance, direction.y*movement_distance, direction.z*movement_distance)
    new_pos = pos+the_offset
    tube_mover.move(new_pos)
    update_pos()
    
def save_offset():
    cur_pos = tube_mover.get_current_pos()
    offset = cur_pos - rack.wells()[0].top().point
    tube_mover.update_offsets_file("x", offset.x)
    tube_mover.update_offsets_file("y", offset.y)
    tube_mover.update_offsets_file("z", offset.z)
    message.set_text("Offset saved {}".format(offset) )

    
    

def show_or_exit(key):
    message.set_text("")
    global movement_distance
    if key in movement_distances.keys():
        set_movement_distance(movement_distances[key])
        
    if key in ('h', 'H'):
        protocol.home()   
        
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop

    if key in ('s', 'S'):
        save_offset()

    if key in ('k', 'K') and movement_distance != "slot":
        set_movement_distance(min(movement_distance,50))
        move_in_direction(types.Point(0,0,1))
        
    if key in ('m', 'M') and movement_distance != "slot":
        set_movement_distance(min(movement_distance,50))
        move_in_direction(types.Point(0,0,-1))
    if key ==  "up" :
        move_in_direction(types.Point(0,1,0))
    if key ==  "down" :
        move_in_direction(types.Point(0,-1,0)) 
    if key ==  "left" :
        move_in_direction(types.Point(-1,0,0))
    if key ==  "right" :
        move_in_direction(types.Point(1,0,0)) 
        
text_header = (u"TubeCheckout Calibration")


header = urwid.AttrWrap(urwid.Text(text_header), 'header')

pos_txt = urwid.Text(('reverse',u"Current position: "))

movement_distance_txt = urwid.Text(('reverse',u"Movement distance: "))

message = urwid.Text(('reverse',u""))


num_key_expl = ", ".join([f"{k}:{movement_distances[k]}mm" for k in movement_distances])
keyboard = urwid.Text(f"""\
KEYBOARD SHORTCUTS:

Number keys - set movement distance: {num_key_expl}

Arrow keys - move horizontally by movement distance
k/m - move vertically up/down by movement distance

s - save calibration (for A1 of tube A1 of slot '5')
h - home
q - exit

""")

instructions = urwid.Text(f"""\
CALIBRATION INSTRUCTIONS

Place a 24 2ml tube rack in slot '5' of the deck.

Place a tube in the gripper and lower it into the top left position, keeping the tube centered in the hole.
Bring the gripper right down vertically such that it just touches the rack. Then save this calibrated position with the 's' key.
""")



blank = urwid.Divider()
div = urwid.Divider(u'-')
content = [blank,pos_txt,blank,movement_distance_txt,blank,message,div,keyboard, div,instructions]
listbox = urwid.Pile(content)
fill = urwid.Filler(listbox, "top")
frame = urwid.Frame(urwid.AttrWrap(fill, 'body'), header=header)
palette = [
        ('body','black','light gray', 'standout'),
        ('reverse','light gray','black'),
        ('header','white','dark red', 'bold'),
        ('important','dark blue','light gray',('standout','underline')),
        ('editfc','white', 'dark blue', 'bold'),
        ('editbx','light gray', 'dark blue'),
        ('editcp','black','light gray', 'standout'),
        ('bright','dark gray','light gray', ('bold','standout')),
        ('buttn','black','dark cyan'),
        ('buttnf','white','dark blue','bold'),
        ]


set_movement_distance(10)
update_pos()
loop = urwid.MainLoop(frame, palette,unhandled_input=show_or_exit)
loop.run()
print("Quitting...")
tube_checkout.utils.watcher_thread.stop()