module line(p1,p2,w) {
    hull() {
        translate(p1) circle(r=w);
        translate(p2) circle(r=w);
    }
}
module polyline(points, index, w) {
    if(index < len(points)) {
        line(points[index - 1], points[index],w);
        polyline(points, index + 1, w);
    }
}

function choose(n, k)=
     k == 0? 1
    : (n * choose(n - 1, k - 1)) / k;

function _point_on_bezier_rec(points,t,i,c)=
    len(points) == i ? c
    : _point_on_bezier_rec(points,t,i+1,c+choose(len(points)-1,i) * pow(t,i) * pow(1-t,len(points)-i-1) * points[i]);

function _point_on_bezier(points,t)=
    _point_on_bezier_rec(points,t,0,[0,0]);

//a bezier curve with any number of control points
//parameters: 
//points - the control points of the bezier curve (number of points is variable)
//resolution - the sampling resolution of the bezier curve (number of returned points)
//returns:
//resolution number of samples on the bezier curve
function bezier(points,resolution)=[
for (t =[0:1.0/resolution:1+1.0/(resolution/2)]) _point_on_bezier(points,t)
];


module tube_hole(radius,top_radius,height, ratio1,ratio2){
resolution = 20;    
$fn = resolution;




p1 = [radius,0];
p2 = [radius,height*ratio1];
p3 = [radius,height*ratio2];
p4 = [top_radius,height];



//translate([0,0,-strength]) cylinder(r=radius+strength,h=strength*2);


points =  bezier([p1,p2,p3,p4],resolution);

points2= concat([[0,0]],points);
points3= concat(points2,[[0,height]]);
echo(points3);
rotate_extrude($fn=60)
polygon(points3);
}

tube_hole(radius=100,top_radius=120,height=100,ratio1=0.5,ratio2=0.7);