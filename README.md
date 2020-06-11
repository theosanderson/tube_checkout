

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

    source_rack = tube_mover.get_rack('1')
    destination_rack = tube_mover.get_rack('2')

    for i, tube in enumerate(source_rack.wells()):
        tube_mover.grab(tube)
        barcode = tube_mover.scan_barcode()
        
        protocol.comment("Tube {} had barcode {}".format(i, barcode))
        
        # Fill in reverse order to avoid collisions
        tube_mover.drop(destination_rack.wells()[23 - i])
```
