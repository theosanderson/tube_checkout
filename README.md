

```py
from opentrons import protocol_api
import tube_checkout

metadata = {
    'protocolName': 'Tube scanning',
    'author': 'John Smith',
    'description': 'Collect each tube in a 24-tube rack, scan the barcode, and drop in a different rack.',
    'apiLevel': '2.2'
}


def run(protocol: protocol_api.ProtocolContext):

    tube_mover = tube_checkout.TubeMover("right")

    source_rack = tube_checkout.load_rack(protocol, '1')
    destination_rack = tube_checkout.load_rack(protocol, '3')

    for i, tube in enumerate(source_rack.wells()):
        tube_mover.grab(tube)
        barcode = tube_mover.scan_barcode()
        
        print("Tube {} had barcode {}".format(i, barcode))
        
        # Fill in reverse order to avoid collisions
        tube_mover.drop(destination_rack.wells()[23 - i])
```
