use <ot_grabber_big.scad>;


offset=120;
height_to_start=20;
overlap=90;
module all_printed_grabber(){
translate([-6,0,offset])
rotate([0,0,180])mount();
translate([-10,-10, height_to_start])
cube([20,20,offset+overlap-height_to_start]);
difference(){ grabber(20);
    translate([-25,-60,0])
   # cube([50,50,70]);
    
}
}

rotate([90,0,0]) all_printed_grabber();