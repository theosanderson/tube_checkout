use <MCAD/nuts_and_bolts.scad>;


dist_y=38;
dist_x=44;
size_x=50;
size_y=80;
thickness=3;

module neg_bit(){
    cylinder(r=1,h=30);
    nutHole(2,tolerance = 0.1);
}



module neg_set(){
    neg_bit();
translate([dist_x,dist_y,0]) neg_bit();

translate([0,dist_y,0]) neg_bit();
translate([dist_x,0,0]) neg_bit();
}


module barcode_mount(){


difference(){
    cube([size_x,size_y,thickness]);
    translate([(size_x-dist_x)/2,5,0])neg_set();

    
}};

barcode_mount();