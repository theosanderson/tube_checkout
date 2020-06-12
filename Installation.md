# Mount the grabber

Using the OpenTrons app connect to your robot and go to `Pipettes and Modules`. Remove the existing pipette on the right mount if present (`Change`), or press `Attach`. The Mount will lower. Choose an arbitary pipette and follow the onscreen instructions, installing the tool as if it were a pipette, using three of the four nut holes. You do not need to connect the wire (there is nothing to connect it to!) so press `Back -> Exit` after the tool is attached. 

# Installing the package

Tube Checkout is a Python package. To install it follow these instructions.

### Find your robot's IP address
Open the OpenTrons app. Go to the Robot tab and click on your Robot. In the `Connectivity` section you will see IP addresses listed for the robot. Choose an IP by which your computer is connected to the robot, i.e. if you are connected to it wirelessly, choose the Wireless IP, if you are connected with a wire choose the wired IP.

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

Place a custom 24 tube rack on position '5' of the robot deck. By hand put a tube into the robot's gripper so that it is hanging vertically down.

Using the arrow keys, the `k` and `m` keys, and `0-9` to choose how far to move, guide the tube to the center of the A1 position (top left) in the tube rack. Once the tube is centered, lower the tool until the base of the tool just touches the rack.

Finally, press the `s` key to save this position, press the `h` key to home the tool, and press `q` to quit the calibration tool.
