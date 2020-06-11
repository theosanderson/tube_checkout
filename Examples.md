# Examples/documentation

To use this package you need to make an instance of the TubeMover class.

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
    # do stuff
```

For convenience TubeMover has a function `get_rack` which will return a Tube Checkout rack labware at the desired deck position. Racks are best supported in positions 1,2, 4 and 5. Other positions may cause collisions.

```py
source_rack = tube_mover.get_rack('1') # Load a rack in slot '1'
```

You can use these racks for conventional pipetting

```py
tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '3')
p300 = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])
p300.aspirate( source_rack['A1'])
```

but you can also pick up tubes from them:

```py
tube_mover.grab(source_rack['A1'])
```

and put them down again

```py
tube_mover.drop(source_rack['A1'])
```

Deck position '6' should be reserved for the barcode scanner. If it's installed there 
(and the USB connected to the robot's USB port), you can use:

```py
tube_mover.grab(source_rack['A1'])
tube_mover.scan_barcode()
tube_mover.drop(source_rack['A1'])
```

We can iterate over positions as normal, note that we need to be careful to collect tubes from top to bottom 
in a column and to drop plates from bottom to top, to leave room for the grabber:
```py
source_rack = tube_mover.get_rack('1') # Load a rack in slot '1'
dest_rack = tube_mover.get_rack('2') # Load a rack in slot '2'

for x in range(6)
  for y in range(4):
    source_position = source_rack.columns()[x][y]
    dest_position = dest_rack.columns()[x][3-y] # We need to fill racks from bottom to top to prevent collisions
    tube_mover.grab(source_position)
    tube_mover.drop(dest_position)
```

If we're trying to fill a 96 well plate it is helpful to combine multiple racks into one conceptual bigger rack. 
The package provides a useful helper class for this, e.g. we can put racks in deck positions 1,2, 4 and 5 as one big rack.

```py
rack_places = ['1', '2', '4', '5']
racks = {x: tube_mover.get_rack(x) for x in rack_places}
import tube_checkout.utils

grid = [ [racks['4'], racks['5'] ],
         [racks['1'],racks['2']] ]
ninetysix_position_rack = tube_checkout.utils.BiggerLabwareFromComponents(grid)   
```

You can then use `ninetysix_position_rack.wells()` or `ninetysix_position_rack['E5']` or `ninetysix_position_rack.columns()[5][5]`.

