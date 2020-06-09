$fn=30;
tube_small_width = 11.3;
tube_big_width = 13.8;
holder_width=20;
holder_extra=14;
holder_length=24;

holder_thickness=2;
tolerance=2;
use <MCAD/nuts_and_bolts.scad>;


module one_neg_bit(){
    cylinder(r=tube_small_width/2,h=5);

translate([-tube_small_width/2,0,0])
cube([tube_small_width,20,25]);


hull(){
translate([-holder_width/2,holder_length-holder_extra,0])
    
cube([holder_width,3,25]);
 cylinder(r=1,h=50);   };
 };
 
 
 module one_neg_bit_for_calibration(){
     calibration_tolerance=0.5;
    cylinder(r=tube_small_width/2-calibration_tolerance,h=5);

translate([-tube_small_width/2+calibration_tolerance,0,0])
cube([tube_small_width-calibration_tolerance*2,20,5]);


hull(){
    
translate([-holder_width/2,holder_length-holder_extra+calibration_tolerance*2,0])
    
cube([holder_width,3,5]);
 cylinder(r=1,h=5);   };
 translate([0,5,-1.5])
 cube([23,20,3],center=true);
 };
 
 
 
 module grabber(grabber_height=7, back_piece = true){
     if(back_piece){
difference(){
    translate([-20/2,-holder_extra,0])
cube([20,4,60]);
    translate([0,0,15])
    rotate([90,0,0])
cylinder(r=2.6,h=50);
      translate([0,0,45])
    rotate([90,0,0])
cylinder(r=2.6,h=50);
    
      translate([0,0,30])
    rotate([90,0,0])
#cylinder(r=2.6,h=50);
}
}

difference(){
    translate([-holder_width/2,-holder_extra,0])
    cube([holder_width,holder_length,grabber_height]);

    one_neg_bit();
    
    translate([-holder_width/2,-holder_extra+17,0])
    #cube([holder_width,holder_length-17,1]);
//translate([-tube_big_width/2,0,3])
//cube([tube_big_width,20,3]);


translate([0,0,holder_thickness])
#cylinder(r1=tube_big_width/2,r2=tube_big_width/2+tolerance,h=5);

translate([0,0,7])
#cylinder(r=tube_big_width/2+tolerance,h=25);


};



};


module smaller(){
    
    one_neg_bit();
}


big_dist_pipette = 89;
small_dist_pipette = 26.3;
size =35;

module copy_mirror(vec=[0,1,0])
{
    children();
    mirror(vec) children();
}


module neg_bit(){
    cylinder(r=1.6,h=30);
    nutHole(3,tolerance = 0.1);
}

module neg_bit2(){
    cylinder(r=2.6,h=30);
    translate([0,0,2])
    cylinder(r=5,h=30);
}


grabber(7);

module pipette_negative(){
copy_mirror(){
    
    translate([0,small_dist_pipette/2,0])
      rotate([0,90,0]) neg_bit();
    
    
       translate([0,small_dist_pipette/2,big_dist_pipette])
      rotate([0,90,0]) neg_bit();
    
    
    translate([0,0,10])  rotate([0,90,0]) neg_bit2();
    
     translate([0,0,70])  rotate([0,90,0]) neg_bit2();
    
}
    
    
}


module mount(){
difference(){
translate([0,-size/2,0])
cube([4,size,100]);
    
    translate([0,0,5])
#pipette_negative();
    
}

};