plate_x=127.76;
plate_y=85.48;
thickness=10;

difference(){
cube([plate_x,plate_y,thickness]);
    
    
    hull(){
        
        #translate([20,20,0])cylinder(r=3,h=20);
        #translate([50,20,0]) cylinder(r=3,h=20);
      #  translate([20,70,0]) cylinder(r=3,h=20);
        
        
    }
    
    
    hull(){
        
        #translate([90,40,0])cylinder(r=3,h=20);
        #translate([110,40,0]) cylinder(r=3,h=20);
      #  translate([110,70,0]) cylinder(r=3,h=20);
        
        
    }
    
    
    hull(){
        
        #translate([90,70,0])cylinder(r=3,h=20);
        #translate([70,20,0]) cylinder(r=3,h=20);
      #  translate([40,70,0]) cylinder(r=3,h=20);
        
        
    }
}



barcode_attachment();
use <barcode_mount.scad>;


module goalpost(){
    
    hull(){
        cylinder(r1=10,r2=5,h=20);  
        
    }
  
    cylinder(r=5,h=55);  
      
      translate([0,0,55]){
      cylinder(r1=5,r2=3,h=5); 
          translate([0,0,5])
          cylinder(r1=3,r2=5,h=5); 
         
         
      
    
      
  };
};


translate([90,30,0])
goalpost();
translate([10,30,0])
rotate([0,0,180])
goalpost();

module barcode_attachment(){
hull(){
translate([110,2,0])
cube([10,30,10]);
translate([145,-70,0])
rotate([0,0,10])
    translate([0,70,30])
    cube([3,20,30]);

}
translate([145,-70,0])
rotate([0,0,10])
    translate([0,0,0])
    cube([3,20,20]);



translate([145,-70,70])
rotate([0,90,10])
barcode_mount();


};
color("blue")
hull(){
       translate([95,18,0])
       cube([24,17,30]); 
    }
    
translate([107,30,33])difference(){
    rotate([0,0,180])
one_neg_bit_for_calibration();
    translate([-30,-30,-10])
    cube([50,19,50]);
    

}
use <ot_grabber_big.scad>;
translate([107,30,33])
rotate([0,0,180])
%grabber();