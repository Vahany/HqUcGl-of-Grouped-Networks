#!/usr/bin/python
"""
  Variant of grid-layout; input is given as containment
  and non-overlap matrices, rather than the graph itself.
"""

import sys
import string
import option

(INEQ, STRICT) = (0, 1)
(LINEAR, QUAD) = (0, 1)
(SYM_NONE, SYM_MIN, SYM_MAX) = (0, 1, 2)
#(POS, POS_AND_DIM) = (0, 1)

class Opt:
  contain = STRICT
  penalty = LINEAR

  ## Objective choices
  penalize_dim = False
  penalize_bound = False
  two_one = False
  aspect = None

  ## Default coefficients
  pos_coeff = 4
  dim_coeff = 1
  bound_coeff = 2

  symbreak = SYM_NONE
  log = False

spec = {
    "-relax-box" : option.setopt("contain", INEQ),
    "-penalize-dim" : option.setopt("penalize_dim", True),
    "-penalize-bound" : option.setopt("penalize_bound", True),
    "-symbreak-min" : option.setopt("symbreak", SYM_MIN),
    "-symbreak-max" : option.setopt("symbreak", SYM_MAX),
    "-quad" : option.setopt("penalty", QUAD),
    "-pos-coeff" : ("pos_coeff", int),
    "-dim-coeff" : ("dim_coeff", int),
    "-bound-coeff" : ("bound_coeff", int),
    "-aspect" : ("aspect", lambda s : tuple(map(int, s.split(':')))),
    "-log" : option.setopt("log", True),
    "-2-1" : option.setopt("two_one", True)
  }


class Model:
  def __init__(self, outfile):
    self.outfile = outfile
    self.nboxes = 0
    self.nbools = 0
    self.nints = 0

  def new_bool(self):
    b = "b{0}".format(self.nbools)
    self.nbools += 1

    print >>self.outfile, "new_bool({0})".format(b)

    return b

  def new_int(self, lo, hi):
    v = "v{0}".format(self.nints)
    self.nints += 1

    print >>self.outfile, "new_int({0}, {1}, {2})".format(v, lo, hi)

    return v
     
  def named_span(self, ident, sz):
    s = "s{0}".format(ident)
    e = "e{0}".format(ident)

    print >>self.outfile, "new_int({0}, 0, {1})".format(s, sz-1)
    print >>self.outfile, "new_int({0}, 0, {1})".format(e, sz-1)

    print >>self.outfile, "int_leq({0}, {1})".format(s, e)

    return (s, e)

  def spanvars(self, sz):
    ident = self.nboxes
    self.nboxes += 1
    return self.named_span(ident, sz)

def read_inst(infile):
  global left
  global above
  (nrows, ncols, nclusters) = map(int, infile.readline().strip().split()[:3])

  ## Read names and dimensions
  dimelts = infile.readline().strip().split()
  nodes = [
      (dimelts[i],
       None if int(dimelts[i+1]) == 0 else (int(dimelts[i+1]), int(dimelts[i+2])))
        for i in xrange(0, len(dimelts), 3) ]

  ## Containment matrix
  # Assumed to be transitively reduced
  containment = []
  for ci in xrange(nclusters):
    crow = map(bool, map(int, infile.readline().strip().split()))
    assert len(crow) == nclusters
    containment += [(ci, cj) for cj in xrange(len(crow)) if crow[cj]]

  ## Non-overlap matrix
  # Also assumed to be minimized.
  nonoverlap = []
  for ci in xrange(nclusters):
    crow = map(bool, map(int, infile.readline().strip().split()))
    assert len(crow) == nclusters
    nonoverlap += [(ci, cj) for cj in xrange(len(crow)) if crow[cj]]

  ## Distance matrix
  dists = [ map(int, infile.readline().strip().split()) for ci in xrange(nclusters) ]
  weights = [ map(int, infile.readline().strip().split()) for ci in xrange(nclusters) ]

  sparse_dists = [ (i, j, dists[i][j], weights[i][j])
      for i in xrange(nclusters) for j in xrange(nclusters)
      if dists[i][j] != 0 ]
  
  #left
  left = []
  myline = infile.readline()
  if (myline):
    for ci in xrange(nclusters):
      crow = map(bool, map(int, myline.strip().split()))
      assert len(crow) == nclusters
      left += [(ci, cj) for cj in xrange(len(crow)) if crow[cj]]
      myline = infile.readline()

  above = []
  if (myline):
    for ci in xrange(nclusters):
      crow = map(bool, map(int, myline.strip().split())) 
      assert len(crow) == nclusters
      above += [(ci,cj) for cj in xrange(len(crow)) if crow[cj]]
      myline= infile.readline()
  
  return (nrows, ncols, nodes, containment, nonoverlap, sparse_dists, left, above)
  
if __name__ == '__main__':
  
  left = []
  above = []
  ## Is the penalty a linear or quadratic?

  args = option.parse_opts(sys.argv[1:], spec, Opt)
  
  if len(args) > 0:
    print "ERROR - Unknown arguments:", args
    sys.exit(1)


#  (LINEAR, QUAD) = (0, 1)
  infile = sys.stdin
  outfile = sys.stdout

  model = Model(outfile)
  # penalty_mode = QUAD
#  penalty_mode = LINEAR

#  if "-lin" in sys.argv:
#    penalty_mode = LINEAR
#  if "-quad" in sys.argv:
#    penalty_mode = QUAD

  (nrows, ncols, nodes, containment, nonoverlap, dists, left, right) = read_inst(infile)
 
  rows = {}
  cols = {}

  ## Top-level nodes are those which aren't contained in
  ## another node.

  #ignore = None
  toplevel = [ n for n in xrange(len(nodes)) if
      len([p for (p, c) in containment if c == n]) == 0 ]


#  for (node, dim) in nodes:
  for node in xrange(len(nodes)):
    dim = nodes[node][1]

    (rs, re) = model.named_span("_r_" + nodes[node][0], nrows)
    (cs, ce) = model.named_span("_c_" + nodes[node][0], ncols)

    rows[node] = (rs, re)
    cols[node] = (cs, ce)

    if dim is not None:
      (w, h) = dim
      if Opt.two_one:
        vw = model.new_int(0,1)
        vh = model.new_int(0,1)
        
        print >>outfile, "int_plus({0},{1},{2})".format(rs,vh, re)
        print >>outfile, "int_plus({0},{1},{2})".format(cs,vw,ce)
        print >>outfile, "int_plus({0},{1},1)".format(vw,vh)
      else:
        print >>outfile, "int_plus({0}, {1}, {2})".format(rs, h-1, re)
        print >>outfile, "int_plus({0}, {1}, {2})".format(cs, w-1, ce)

  if Opt.contain == INEQ:
    for (node, child) in containment:
      (rs, re) = rows[node]
      (cs, ce) = cols[node]

      (c_rs, c_re) = rows[child]
      (c_cs, c_ce) = cols[child]
      
      ## Each child is contained in the parent
      for (x, y) in [(rs, c_rs), (c_re, re), (cs, c_cs), (c_ce, ce)]:
        print >>outfile, "int_leq({0}, {1})".format(x, y)
  else:
    for node in xrange(len(nodes)):
      children = [ child for (n, child) in containment if n == node ]

      if len(children) == 0:
        continue

      # print >>sys.stderr, node, children
      (rs, re) = rows[node]
      (cs, ce) = cols[node]

      c_rss = [ rows[child][0] for child in children ]
      c_res = [ rows[child][1] for child in children ]
      c_css = [ cols[child][0] for child in children ]
      c_ces = [ cols[child][1] for child in children ]

      ## Parent is the bounding box of the children.
      for (x, op, ys) in [(rs, "min", c_rss), (re, "max", c_res),
                          (cs, "min", c_css), (ce, "max", c_ces)]:
        print >>outfile, "int_array_{1}([{2}], {0}).".format(x, op, ",".join(ys))

  for (nx, ny) in nonoverlap:
    (x_rs, x_re) = rows[nx]
    (x_cs, x_ce) = cols[nx]

    (y_rs, y_re) = rows[ny]
    (y_cs, y_ce) = cols[ny]
    
     
    if (nx,ny) in left:
        print >>outfile, "int_lt({0}, {1})".format(x_ce, y_cs)
    elif (ny,nx) in left:
        print >>outfile, "int_lt({0}, {1})".format(y_ce, x_cs)
    elif (nx,ny) in above:
        print >>outfile, "int_lt({0}, {1})".format(x_re, y_rs)
    elif (ny,nx) in above:
        print >>outfile, "int_lt({0}, {1})".format(y_re, x_rs)
    else:
      ## Direct children cannot overlap
      [cxy, cyx, rxy, ryx] = seps = [model.new_bool() for i in xrange(4)]
    
      for (u, v, w) in [(x_re, y_rs, rxy), (y_re, x_rs, ryx), (x_ce, y_cs, cxy), (y_ce, x_cs, cyx)]:
        print >>outfile, "int_lt_reif({0}, {1}, {2})".format(u, v, w)

      print >>outfile, "bool_array_or([{0}])".format(",".join(seps))

  ## Symmetry breaking
  if Opt.symbreak != SYM_NONE:
    # Pick an arbitrary pair of nodes.
    (nx, ny) = min(nonoverlap) if Opt.symbreak == SYM_MIN else max(nonoverlap)
    if Opt.log:
      print >>sys.stderr, "Breaking symmetry on", (nx, ny)

    (x_rs, x_re) = rows[nx]
    (x_cs, x_ce) = cols[nx]

    (y_rs, y_re) = rows[ny]
    (y_cs, y_ce) = cols[ny]

    for (u, v) in [(x_rs, y_rs), (x_re, y_re)]:
      print >>outfile, "int_leq({0}, {1})".format(u, v)

  ## Handle differences 
  diffs = []

  ## Compute the distance penalty for each pair of edges
  wmax = 0
  for (x, y, dopt, weight) in dists:
    (x_rs, x_re) = rows[x]
    (x_cs, x_ce) = cols[x]

    (y_rs, y_re) = rows[y]
    (y_cs, y_ce) = cols[y]

    rxy = model.new_int(-nrows, nrows)
    ryx = model.new_int(-nrows, nrows)

    cxy = model.new_int(-ncols, ncols)
    cyx = model.new_int(-ncols, ncols)

    ## Connect the signed differences to the values
    for (u, v, z) in [(x_re, rxy, y_rs), (y_re, ryx, x_rs), (x_ce, cxy, y_cs), (y_ce, cyx, x_cs)]:
      print >>outfile, "int_plus({0}, {1}, {2})".format(u, v, z)

    dr = model.new_int(0, nrows)
    dc = model.new_int(0, ncols)
    
    ## Compute the concrete values.
    print >>outfile, "int_array_max([0, {0}, {1}], {2})".format(rxy, ryx, dr)
    print >>outfile, "int_array_max([0, {0}, {1}], {2})".format(cxy, cyx, dc)

    sign_penalty = model.new_int(-dopt, nrows+ncols-dopt)
    pmax = max(dopt, nrows+ncols-dopt)
    penalty = model.new_int(0, pmax)

    print >>outfile, "int_array_plus([{0}, {1}, {2}], {3})".format(dr, dc, -dopt, sign_penalty)
    print >>outfile, "int_abs({0}, {1})".format(sign_penalty, penalty)


    if Opt.penalty == LINEAR:
      weighted_penalty = model.new_int(0, weight*pmax)
      wmax += weight*pmax
      print >>outfile, "int_times({0}, {1}, {2})".format(weight, penalty, weighted_penalty)
      diffs.append(weighted_penalty)
    else:
      quad_penalty = model.new_int(0, weight*pmax*pmax)
      wmax += weight*pmax*pmax
      for ii in xrange(pmax):
        channel = model.new_bool()
        print >>outfile, "int_leq_reif({0}, {1}, {2})".format(penalty, ii, channel)
        print >>outfile, "int_leq_reif({0}, {1}, {2})".format(quad_penalty, weight*ii*ii, channel)
      diffs.append(quad_penalty)

  ## Weak bounds on w.
  print >>outfile, "new_int(p_pos, 0, {0})".format(wmax)

  ## Connect w to the distance penalties
  print >>outfile, "int_array_plus([{0}], p_pos)".format(",".join(diffs))

  obj = [("p_pos", Opt.pos_coeff, 0, wmax)]

  ## Are we incorporating cluster size into the objective?
  if Opt.penalize_dim:
    ## Figure out the dimension/pos coefficients.

    ## Compute width and height for each non-leaf node.
    ## Currently weak bounds.
    def mk_diff(svar, evar, vmax):
      v = model.new_int(0, vmax)
      print >>outfile, "int_plus({1}, {2}, {0})".format(evar, svar, v)
      return v
    
    dmin = 0
    dmax = nrows*len(rows) + ncols*len(cols)

    rdims = [ mk_diff(rows[n][0], rows[n][1], nrows) for n in rows if n not in toplevel]
    cdims = [ mk_diff(cols[n][0], cols[n][1], ncols) for n in cols if n not in toplevel]
    print >>outfile, "new_int(p_dim, {0}, {1})".format(dmin, dmax)
    print >>outfile, "int_array_plus([{0}], p_dim)".format(",".join(rdims+cdims))
    
    obj.append( ("p_dim", Opt.dim_coeff, dmin, dmax) )

  ## Do we have a penalty term for the maximum size?
  if Opt.penalize_bound:
    rmax = model.new_int(0, nrows)
    cmax = model.new_int(0, ncols)
    print >>outfile, "int_array_max([{0}], {1})".format(",".join([rows[n][1] for n in rows if n in toplevel]), rmax)
    print >>outfile, "int_array_max([{0}], {1})".format(",".join([cols[n][1] for n in cols if n in toplevel]), cmax)

    ## Do we have an aspect-ratio constraint?
    ## Aspect is only meaningful if we're penalizing the bounds.
    if Opt.aspect is not None:
      (cy, cx) = Opt.aspect

      bmin = 0
      bmax = ncols
      print >>outfile, "int_array_lin_leq([{0},{1}], [{2},{3}], 0)".format(cy, -cx, rmax, cmax)
      print >>outfile, "new_int(p_bound, {0}, {1})".format(bmin, bmax)
      print >>outfile, "int_eq({0}, p_bound)".format(cmax)
    else:
      bmin = 0
      bmax = nrows + ncols

      print >>outfile, "new_int(p_bound, {0}, {1})".format(bmin, bmax)
      print >>outfile, "int_plus({0}, {1}, p_bound)".format(rmax, cmax)

    obj.append( ("p_bound", Opt.bound_coeff, bmin, bmax) )
    
  ## Now we compute the objective
  if len(obj) == 1:
    ## If there's only one term, we can safely discard the coefficients.
    (term, _, low, high) = obj[0]
    print >>outfile, "new_int(w, {0}, {1})".format(low, high)
    print >>outfile, "int_eq(w, {0})".format(term)
  else:
    terms = [ term for (term, _, _, _) in obj ]
    coeffs = [ coeff for (_, coeff, _, _) in obj ]
    wlb = sum([coeff*lb for (_, coeff, lb, _) in obj])
    wub = sum([coeff*ub for (_, coeff, _, ub) in obj])
        
    print >>outfile, "new_int(w, {0}, {1})".format(wlb, wub)
    print >>outfile, "int_array_lin_eq([{0}], [{1}], w)".format(",".join(map(str,coeffs)), ",".join(terms))

  print "solve minimize w"
