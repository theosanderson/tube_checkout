$fn=50;
tube_od= 12;
tolerance=0;
dist_centers=20;
num_x=6;
num_y=4;
plate_x=127.76;
plate_y=85.48;
offset_x=(plate_x-(num_x-1)*dist_centers)/2;
offset_y=(plate_y-(num_y-1)*dist_centers)/2;
offset_z=2;
total_thickness=29+offset_z;

cone_height=5;
cone_extra=4.5;

cut_out_dim=5;

use <barcode_mount.scad>;
use <tube_shape.scad>;
module neg_tube2(){
    cylinder(r=tube_od/2+tolerance/2,h=50);
    
    translate([0,0,total_thickness-offset_z-cone_height])
    cylinder(r1=tube_od/2+tolerance/2,r2=tube_od/2+tolerance/2+cone_extra,h=cone_height);
    ;
    
     translate([0,0,total_thickness-offset_z-cone_height-2])
   # cylinder(r1=tube_od/2+tolerance/2,r2=tube_od/2+tolerance/2+0.75,h=4);
    ;
}

module neg_tube(){
    #tube_hole(radius=tube_od/2+tolerance/2,top_radius=tube_od/2+tolerance/2+cone_extra, height=29,ratio1=0.8,ratio2=0.9);

}



module neg_set(){
for (x = [0:num_x-1]){
    for (y = [0:num_y-1]){
        translate([x*dist_centers,y*dist_centers,0])
        neg_tube();
    
}
}
};

module rack(){
difference(){
cube([plate_x,plate_y,total_thickness]);
translate([offset_x,offset_y,offset_z])
neg_set();
    translate([0,plate_y-cut_out_dim/2,0])
    rotate([0,0,45])
    
   # cube([cut_out_dim,cut_out_dim,50]);
   
};

};

rotate([0,180,0]) rack();


//barcode_attachment();

module barcode_attachment(){
translate([125,-10,10])
cube([15,30,20]);

translate([140,-70,50])
rotate([0,90,0])
barcode_mount();
};