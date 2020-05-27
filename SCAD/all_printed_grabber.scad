use <ot_grabber_big.scad>;
offset=90;
height_to_start=40;
overlap=90;
translate([-6,0,offset])
rotate([0,0,180])mount();
translate([-10,-10, height_to_start])
cube([20,20,offset+overlap-height_to_start]);
grabber();