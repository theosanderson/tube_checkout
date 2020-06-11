# Tube Checkout

Tube Checkout is an open hardware extension for [OpenTrons OT2](http://opentrons.com) liquid handling robots, which allows them to carry tubes and scan barcodes from them using a 3D printed tool that occupies one of the two pipette mounts.

Tube Checkout currently works with Sarstedt 2ml screw-capped tubes. Tube Checkout allows you to write a protocol which records the identity of each tube loaded onto the robot deck, transfers liquid from these tubes into a plate, and writes out the identity of the liquid in each well of the plate. It thus forms a bridge between operations performed per-sample (e.g. collection of saliva) and those performed in batches (e.g. RNA extraction). The hardware for Tube Checkout is 3D printed, and the materials and the barcode scanner together cost <$50.

Here is an example protocol which scans 24 tubes:

```py
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


### Getting started
