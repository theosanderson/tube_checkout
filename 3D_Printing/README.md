# 3D Printing

All files are designed for printing with an FDM printer. While SLA printing is likely possible it will require some modifications to the SCAD files. The orientation of the printing files is that which we feel works best.

### Grabbing tool

Print [all_printed_grabber.stl](all_printed_grabber.stl) with support. It is best to use a low (0.1) layer height, or to use adaptive layer heights.

Once printed clear the nut holes and put some M3 nuts into them. You can use a spare M3 bolt to tighten the nuts into the holes.

### Racks

Print either [24_2ml_tube_rack_v2.stl](24_2ml_tube_rack_v2.stl) (easier to print) or [24_2ml_tube_rack_v2.2.stl](24_2ml_tube_rack_v2.2.stl) (functionally better, more tolerance). The files are set up to print the rack upside-down because this gives the flattest bottom, which is where tolerance is most crucial. Feel free to try printing the other way too if you are confident about your printbed. They should be printed *without* support. To keep the rings smooth it may be worth printing quite slowly. A low infill is fine.

### Barcode scanner mount

Print [barcode_plate.stl](https://github.com/theosanderson/tube_checkout/blob/master/SCAD/barcode_plate.stl) with support. This prints right-way-up so you may need to clean up the sides at the bottom with a knife if the bottom layer is too fat. Attach a rubber band across the goalposts (double up until it is somewhat taut), and attach the barcode scanner to the mount either with tape or M2 nuts and bolts.

You probably want to put the barcode scanner it automatic mode (always on) by printing out the `Automatic successive` barcode in [the manual](https://github.com/theosanderson/tube_checkout/blob/master/Documentation/Hardware/MagicBarcodes.pdf).
