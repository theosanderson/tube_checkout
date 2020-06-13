# Tube Checkout

Tube Checkout is an open hardware extension for [OpenTrons OT2](http://opentrons.com) liquid handling robots, which allows them to carry tubes and scan barcodes from them using a 3D printed tool that occupies one of the two pipette mounts.

Tube Checkout currently works with Sarstedt 2ml screw-capped tubes. Tube Checkout allows you to write a protocol which records the identity of each tube loaded onto the robot deck, transfers liquid from these tubes into a plate, and writes out the identity of the liquid in each well of the plate. It thus forms a bridge between operations performed per-sample (e.g. collection of saliva) and those performed in batches (e.g. RNA extraction). The hardware for Tube Checkout is 3D printed, and the materials and the barcode scanner together cost <$50.

Here is an example protocol which scans 24 tubes in about 6 minutes:

```py
def run(protocol: protocol_api.ProtocolContext):

    tube_mover = tube_checkout.TubeMover(protocol)

    source_rack = tube_mover.get_rack('1')
    destination_rack = tube_mover.get_rack('2')
    barcode_file = open("/data/barcodes.txt", "w") 
    for i, tube in enumerate(source_rack.wells()):
        tube_mover.grab(tube)
        barcode = tube_mover.scan_barcode()
        
        barcode_file.write("Tube {} had barcode {}\n".format(i, barcode))
        
        # Fill in reverse order to avoid collisions
        tube_mover.drop(destination_rack.wells()[23 - i])
```


### Getting started
- You will need [some 3D printed parts](3D_Printing/README.md), an [Alacrity Mini Barcode Scanner](https://www.amazon.co.uk/gp/product/B07CXXVLSD/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1) (if you want to scan barcodes), a few M3 nuts, a rubber band, and some [Sarstedt screwcapped 2ml microtubes](https://www.fishersci.com/shop/products/2ml-sc-mtube-cbs-gwb-st-cs1000/50809242) to move around.
- [Mount the tool to the robot, install the Python package, and calibrate the tool](Installation.md).
- View some [examples](Examples.md) of how to use the package in your OpenTrons protocols.
- be aware of the [limitations](https://github.com/theosanderson/tube_checkout/blob/master/limitations_and_mitigation.md) for weirdly-labelled tubes
