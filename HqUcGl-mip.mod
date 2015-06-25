/*********************************************
 * OPL 12.6.1.0 Model
 *********************************************/
int nv =...;
int maxwidth =...;
int maxheight =...;
float bigM = 3.0*maxl(maxwidth,maxheight); 
range vertices = 1..nv;
int swd[vertices]=...;
int sht[vertices]=...;
float dd[vertices,vertices]=...;
float ddw[vertices,vertices]=...;
int containment[vertices,vertices]=...;
int noverlap[vertices,vertices]=...;
dvar int wd[vertices] in 1..maxwidth;
dvar int ht[vertices] in 1..maxheight;
dvar int maxX in 0..maxwidth;
dvar int maxY in 0..maxheight;
dvar float+ x[vertices] in 0..maxwidth;
dvar float+ y[vertices] in 0..maxheight;
dvar int xs[vertices] in 0..maxwidth;
dvar int xf[vertices] in 0..maxwidth;
dvar int ys[vertices] in 0..maxheight;;
dvar int yf[vertices] in 0..maxheight;;
dvar boolean left[vertices,vertices];
dvar boolean xoverlap[vertices,vertices];
dvar boolean right[vertices,vertices];
dvar boolean below[vertices,vertices];
dvar boolean yoverlap[vertices,vertices];
dvar boolean above[vertices,vertices];
dvar float+ xDist[vertices,vertices] in 0..maxwidth;
dvar float+ yDist[vertices,vertices] in 0..maxheight;
dvar float+ dist[vertices,vertices] in -1*(maxwidth+maxheight)..(maxwidth+maxheight);                                  
dvar float+ absdist[vertices,vertices] in 0..maxwidth+maxheight;
dvar boolean b;
dvar boolean bxs[vertices,vertices];
dvar boolean bxf[vertices,vertices];
dvar boolean bys[vertices,vertices];
dvar boolean byf[vertices,vertices];
dvar int bbxs[vertices];
dvar int bbxf[vertices];
dvar int bbys[vertices];
dvar int bbyf[vertices];
dvar float+ thestress;
dvar float+ thesize;

minimize 4*thestress+1*thesize+2*maxX;

subject to {
  forall (u in vertices : swd[u] != 0)
    wd[u] <= swd[u];
  forall (u in vertices : swd[u] != 0)
    wd[u] >= swd[u];
  forall (u in vertices : sht[u] != 0)
    ht[u] <= sht[u];
  forall (u in vertices : sht[u] != 0)
    ht[u] >= sht[u];
      
  forall (u in vertices)
    wd[u] <= xf[u] - xs[u];
  forall (u in vertices)
    wd[u] >= xf[u] - xs[u];
  forall (u in vertices)
    ht[u] <= yf[u] - ys[u];
  forall (u in vertices)
    ht[u] >= yf[u] - ys[u];
  
  forall (u in vertices)
    x[u] <= xs[u] + 0.5 * wd[u];
  forall (u in vertices)
    x[u] <= xf[u] - 0.5 * wd[u];
  forall (u in vertices)
    y[u] <= ys[u] + 0.5 * ht[u];
  forall (u in vertices)
    y[u] <= yf[u] - 0.5 * ht[u];
  forall (u in vertices)
    x[u] >= xs[u] + 0.5 * wd[u];
  forall (u in vertices)
    x[u] >= xf[u] - 0.5 * wd[u];
  forall (u in vertices)
    y[u] >= ys[u] + 0.5 * ht[u];
  forall (u in vertices)
    y[u] >= yf[u] - 0.5 * ht[u];
    
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    xs[u] <= xs[v]; 
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    -bigM*(1-bxs[u,v]) +xs[v] <= xs[u]; 
  forall (u in vertices, v in vertices : containment[u,v] == 0)
    bxs[u,v]<=0;
  forall (u in vertices) bbxs[u] <= sum(v in vertices)(bxs[u,v]);
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    bbxs[u] >=1; 
  forall (u in vertices, v in vertices : containment[u,v] == 0)
    bxs[u,v]>=0;
  forall (u in vertices) bbxs[u] >= sum(v in vertices)(bxs[u,v]);
    
forall (u in vertices, v in vertices : containment[u,v] == 1)
    xf[v] <= xf[u]; 
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    -bigM*(1-bxf[u,v]) +xf[u] <= xf[v]; 
  forall (u in vertices, v in vertices : containment[u,v] == 0)
    bxf[u,v]<=0;
  forall (u in vertices) bbxf[u] <= sum(v in vertices)(bxf[u,v]);
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    bbxf[u] >=1; 
  forall (u in vertices, v in vertices : containment[u,v] == 0)
    bxf[u,v]>=0;
  forall (u in vertices) bbxf[u] >= sum(v in vertices)(bxf[u,v]);
    
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    ys[u] <= ys[v]; 
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    -bigM*(1-bys[u,v]) +ys[v] <= ys[u]; 
  forall (u in vertices, v in vertices : containment[u,v] == 0)
    bys[u,v]<=0;
  forall (u in vertices) bbys[u] <= sum(v in vertices)(bys[u,v]);
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    bbys[u] >=1; 
  forall (u in vertices, v in vertices : containment[u,v] == 0)
    bys[u,v]>=0;
  forall (u in vertices) bbys[u] >= sum(v in vertices)(bys[u,v]);
    
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    yf[v] <= yf[u]; 
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    -bigM*(1-byf[u,v]) +yf[u] <= yf[v]; 
  forall (u in vertices, v in vertices : containment[u,v] == 0)
    byf[u,v]<=0;
  forall (u in vertices) bbyf[u] <= sum(v in vertices)(byf[u,v]);
  forall (u in vertices, v in vertices : containment[u,v] == 1)
    bbyf[u] >=1; 
  forall (u in vertices, v in vertices : containment[u,v] == 0)
    byf[u,v]>=0;
  forall (u in vertices) bbyf[u] >= sum(v in vertices)(byf[u,v]); 
    
  forall (u in vertices, v in vertices)
    -bigM*(1-left[u,v]) + xf[u] <= xs[v]; 
  forall (u in vertices, v in vertices)
    -bigM*(1-right[u,v]) + xf[v] <= xs[u];   
  forall (u in vertices, v in vertices)
    -bigM*(1-xoverlap[u,v]) + xs[u] <= xf[v];   
  forall (u in vertices, v in vertices)
    -bigM*(1-xoverlap[u,v]) + xs[v] <= xf[u]; 
    
  forall (u in vertices, v in vertices)
    -bigM*(1-below[u,v]) + yf[u] <= ys[v]; 
  forall (u in vertices, v in vertices)
    -bigM*(1-above[u,v]) + yf[v] <= ys[u];   
  forall (u in vertices, v in vertices)
    -bigM*(1-yoverlap[u,v]) + ys[u] <= yf[v];   
  forall (u in vertices, v in vertices)
    -bigM*(1-yoverlap[u,v]) + ys[v] <= yf[u]; 
  
  forall (u in vertices, v in vertices)
    left[u,v] + xoverlap[u,v] + right[u,v] <= 1; 
  forall (u in vertices, v in vertices)
    above[u,v] + yoverlap[u,v] + below[u,v] <= 1; 
  forall (u in vertices, v in vertices)
    left[u,v] + xoverlap[u,v] + right[u,v] >= 1; 
  forall (u in vertices, v in vertices)
    above[u,v] + yoverlap[u,v] + below[u,v] >= 1; 
    
  forall (u in vertices, v in vertices : noverlap[u,v] == 1)
    left[u,v] + right[u,v] + below[u,v] + above[u,v] >= 1;   
  forall (u in vertices, v in vertices : noverlap[u,v] == 1)
    xoverlap[u,v] + yoverlap[u,v] <= 1;
    
  forall (u in vertices, v in vertices : containment[u,v] == 1 || containment[v,u]==1)
    xoverlap[u,v] + yoverlap[u,v] <= 2;
  forall (u in vertices, v in vertices : containment[u,v] == 1 || containment[v,u]==1)
    xoverlap[u,v] + yoverlap[u,v] >= 2;
  
  forall (u in vertices, v in vertices)
    xs[v] - xf[u] + 1 <= xDist[u,v];
  forall (u in vertices, v in vertices)
    xs[u] - xf[v] + 1 <= xDist[u,v];
  forall (u in vertices, v in vertices)
    -bigM * (1-xoverlap[u,v]) + xDist[u,v] <= 0.0;
  forall (u in vertices, v in vertices)
    -bigM * (1-left[u,v]) + xDist[u,v] <= xs[v]-xf[u]+1;
  forall (u in vertices, v in vertices)
    -bigM * (1-right[u,v]) + xDist[u,v] <= xs[u]-xf[v]+1;
    
  forall (u in vertices, v in vertices)
    ys[v] - yf[u] + 1 <= yDist[u,v];
  forall (u in vertices, v in vertices)
    ys[u] - yf[v] + 1 <= yDist[u,v];
  forall (u in vertices, v in vertices)
    -bigM * (1-yoverlap[u,v]) + yDist[u,v] <= 0.0;
  forall (u in vertices, v in vertices)
    -bigM * (1-below[u,v]) + yDist[u,v] <= ys[v]-yf[u]+1;
  forall (u in vertices, v in vertices)
    -bigM * (1-above[u,v]) + yDist[u,v] <= ys[u]-yf[v]+1; 
  
  forall (u in vertices, v in vertices)
    dist[u,v] <= xDist[u,v] + yDist[u,v];
  forall (u in vertices, v in vertices)
    dist[u,v] >= xDist[u,v] + yDist[u,v];
  forall (u in vertices, v in vertices)
    -bigM*(1-b) + absdist[u,v] <= (dist[u,v] -dd[u,v]);
  forall (u in vertices, v in vertices)
    -bigM*(1-(1-b)) + absdist[u,v] <= -(dist[u,v] -dd[u,v]);
  forall (u in vertices, v in vertices)
    dist[u,v] -dd[u,v] <= absdist[u,v];
  forall (u in vertices, v in vertices)
    -(dist[u,v] -dd[u,v]) <= absdist[u,v];
    
  thestress <= sum(u,v in vertices)(ddw[u,v]*absdist[u,v]);
  thesize <= sum(u in vertices)(wd[u]+ht[u]);
  
  thestress >= sum(u,v in vertices)(ddw[u,v]*absdist[u,v]);
  thesize >= sum(u in vertices)(wd[u]+ht[u]);
      
  maxY <= 1 * maxX;
  forall (u in vertices)0<=xs[u];
  forall (u in vertices)xf[u]<=maxX;
  forall (u in vertices)0<=ys[u];
  forall (u in vertices)yf[u]<=maxY;
    
}