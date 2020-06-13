# Mount the grabber

Using the OpenTrons app connect to your robot and go to `Pipettes and Modules`. Remove the existing pipette on the right mount if present (`Change`), or press `Attach`. The Mount will lower. Choose an arbitary pipette and follow the onscreen instructions, installing the tool as if it were a pipette, using three of the four nut holes. You do not need to connect the pipette wire (there is nothing to connect it to!) so press `Back -> Exit` after the tool is attached. 

# Installing the package

Tube Checkout is a Python package. Here is how to install it on your robot:

### Find your robot's IP address
Open the OpenTrons app. Go to the `Robot` tab and click on your robot. In the `Connectivity` section you will see IP addresses listed for the robot. Choose the IP by which your computer is connected to the robot, i.e. if you are connected to it wirelessly, choose the `Wireless IP`, if you are connected with a wire choose the `Wired IP`.

Copy this IP address.


### Launch Jupyter

Go to your web browser and go to `http://[YOUR ROBOTIC IP ADDRESS]:48888`. This should load the robot's Jupyter homepage.

### Open a terminal

On the right side of the Jupyter screen press `New` - > `Terminal`. A terminal will appear. 


### Install the package
Click on the black terminal and type `pip install tube-checkout` and press enter.

The package should install.

# Calibrating the tool

Still at the terminal, enter the command `python -m tube_checkout.calibration` and press enter.

The calibration tool will load and the robot will home.

Place a custom 24 tube rack on position '5' of the robot deck. By hand place a tube into the gripper so that it is hanging vertically down.

Using the arrow keys, the `k` and `m` keys, and `0-9` to choose how far to move, guide the tube to the center of the A1 position (top left) in the tube rack. Once the tube is centered, lower the tool until the base of the tool just touches the top of the rack.

Finally, press the `s` key to save this position, press the `h` key to home the tool, and press `q` to quit the calibration tool.

# You're done
Now you are ready to get started. Restart your robot and write a protocol that uses Tube Checkout:

```py
from opentrons import protocol_api
import tube_checkout

metadata = {
    'protocolName': 'Tube scanning',
    'description': 'Collect each tube in a 24-tube rack, scan the barcode, and drop in a different rack.',
    'apiLevel': '2.2'
}


def run(protocol: protocol_api.ProtocolContext):

    tube_mover = tube_checkout.TubeMover(protocol)
    rack = tube_mover.get_rack('1') # Load a rack in slot '1'
    tube_mover.grab(rack['A1'])
    tube_mover.scan_barcode()
    tube_mover.drop(rack['A1'])
```

Note that the calibration we have done only applies to the grabbing tool - you will also need to calibrate the rack labware in the OpenTrons app for pipettes to be able to access it properly.
