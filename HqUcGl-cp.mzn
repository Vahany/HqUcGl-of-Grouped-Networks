include "globals.mzn";

% number of vertices
int: nv;
set of int: vertices = 1..nv;
constraint assert(nv >= 2, "need at least two vertices");
% defined width & height of each vertex
array[vertices] of 0..maxwidth : swd;
array[vertices] of 0..maxheight : sht;
% calculated width & height of each vertex
array[vertices] of var 1..maxwidth: wd;
array[vertices] of var 1..maxheight: ht;
% if defined width & height are not 0, assign to calculated width & height
constraint (forall (u in vertices where swd[u] != 0)(wd[u] = swd[u]));
constraint (forall (u in vertices where sht[u] != 0)(ht[u] = sht[u])); 
% desired (Manhattan) distance and weight between each pair of vertices
array[vertices,vertices] of 0..(maxwidth+maxheight): dd;
array[vertices,vertices] of int: ddw;
constraint 
assert(forall(u,v in vertices where u!=v)(dd[u,v] >= 0), "dd should be >=0");
constraint 
assert(forall(u,v in vertices where u!=v)(ddw[u,v] >= 0), "ddw should be >=0");
% containment matrix for each pair of vertices
array[vertices,vertices] of bool : containment;
% non-overlap matrix for each pair of vertices : 0 if they should overlap and 1 if they should not
array[vertices,vertices] of bool : noverlap; 
% maximum starting width & height of grid
int: maxwidth;
int: maxheight;
int : ar = 1;
var int : maxX;
var int : maxY;
constraint 0 <= maxX /\ maxX <= maxwidth;
constraint maxY <= ar * maxX;
% core decision variables
% vertex position
array[vertices] of var 0..maxwidth: xs;
array[vertices] of var 0..maxwidth: xf;
array[vertices] of var 0..maxheight: ys;
array[vertices] of var 0..maxheight: yf;
constraint forall(u in vertices)(xf[u] = xs[u]+wd[u]); 
constraint forall(u in vertices)(yf[u] = ys[u]+ht[u]); 
%symmetry constraint
int : smallu = min([u | u in vertices where exists(v in vertices)(noverlap[u,v])]);
int : smallv = min([v | v in vertices where exists(u in vertices)(noverlap[u,v])]);
constraint xs[smallu] <= xs[smallv] /\ ys[smallu] <= ys[smallv];
% some vertices should not overlap
constraint
forall(u,v in vertices where u < v /\ noverlap[u,v])(nonOverlap(u,v));
predicate nonOverlap(vertices: u, vertices:v) =
 ((xf[u] <= xs[v]) \/ (xf[v] <= xs[u]) \/ (yf[u] <= ys[v]) \/ (yf[v] <= ys[u]));
% all vertices contained in their parent container
constraint
forall(u in vertices where exists(v in vertices)(containment[u,v])) (
  xs[u] = min([xs[v]|v in vertices where containment[u,v]]) /\
  xf[u] = max([xf[v]|v in vertices where containment[u,v]]) /\
  ys[u] = min([ys[v]|v in vertices where containment[u,v]]) /\
  yf[u] = max([yf[v]|v in vertices where containment[u,v]]));
% all vertices are in the drawing area
constraint
forall(v in vertices)(
 0 <= xs[v] /\ xf[v] <= maxX);
constraint
forall(v in vertices)(
 0 <= ys[v] /\ yf[v] <= maxY);
% distance between vertices 
array[vertices,vertices] of var 0..maxwidth: xAbsDist;
array[vertices,vertices] of var 0..maxheight: yAbsDist;
constraint
forall(u,v in vertices where u<v) (
 xAbsDist[u,v]= max([0,xs[v]-xf[u]+1,xs[u]-xf[v]+1]) /\ 
 yAbsDist[u,v]= max([0,ys[v]-yf[u]+1,ys[u]-yf[v]+1]));
% Manhattan stress
array[vertices,vertices] of var 0..(2*(maxwidth+maxheight)): absdist;
constraint
forall(u,v in vertices where u<v) (
  absdist[u,v] = abs(xAbsDist[u,v]+yAbsDist[u,v]-dd[u,v]));
var int: stress = sum(u,v in vertices)((ddw[u,v])*(absdist[u,v])); 
var int: size = sum(u in vertices)(wd[u]+ht[u]);
var int: M = (4*stress)+(1*size)+(2*maxX);

solve
minimize M; 


