#!/usr/bin/python
"""
  Take a modgraph file, and output a dense representation
  with overlap and containment graphs.
"""
import sys
from parsemod import read_graph

## Flags for ideal distance computation
(DIRECT, TRANSITIVE) = (0, 1)

def compute_parents(nodes):
  parent = { node : None for (node, _, _) in nodes }
  for (node, children, _) in nodes:
    for child in children:
      parent[child] = node
  return parent

def compute_grid(nodes, ggrids):
  def dkey(ni, nj):
    return (nodes[ni][0], nodes[nj][0])
  nnodes = len(nodes)
  inv = {nodes[ni][0] : ni for ni in xrange(nnodes) }
  grids = { dkey(inv[ni], inv[nj]) for (ni, nj) in ggrids }
  return grids


def compute_ideal(nodes, ddists, comp = DIRECT):
  def dkey(ni, nj):
    (ni, nj) = (ni, nj) if ni < nj else (nj, ni)
    return (nodes[ni][0], nodes[nj][0])

  ## Naive implementation; just does Floyd-Warshall
  nnodes = len(nodes)
  inv = { nodes[ni][0] : ni for ni in xrange(nnodes) }
  dists = { dkey(inv[ni], inv[nj]) : d for (ni, nj, d) in ddists }
    
  if comp == DIRECT:
    return dists

  for (node, _, _) in nodes:
    dists[(node, node)] = 0

  parent = compute_parents(nodes)

  ## Standard Floyd-Warshall, with the addition that we
  ## never propagate distances between parents and children.
  for nk in xrange(nnodes):
    for ni in xrange(nnodes):
      if dkey(ni, nk) not in dists:
        continue
      dik = dists[dkey(ni, nk)]

      for nj in xrange(nnodes):
        if dkey(nk, nj) not in dists:
          continue
        dkj = dists[dkey(nk, nj)]

        if dkey(ni, nj) in dists:
          old_dij = dists[dkey(ni, nj)]
          dists[dkey(ni, nj)] = min(old_dij, dik + dkj)
        else:
          if nodes[ni][0] == parent[nodes[nj][0]] or nodes[nj][0] == parent[nodes[ni][0]]:
            continue
          dists[dkey(ni, nj)] = dik + dkj
        
  return dists

if __name__ == "__main__":
  dist_model = DIRECT
#  dist_model = TRANSITIVE

  infile = sys.stdin

  (nrows, ncols, nodes, dists, lefts, aboves) = read_graph(infile)
  nnodes = len(nodes)

  print nrows, ncols, nnodes
  
  ## Node dimensions
  dims = []
  for (node, _, dim) in nodes:
    if dim is None:
      dims.append( (node, (0, 0)) )
    else:
      dims.append( (node, dim) )

  ## Output node dimensions
  print " ".join(" ".join(map(str,[node, w, h])) for (node, (w, h)) in dims)

  ## Output containment matrix
  for (_, children, _) in nodes:
    print " ".join("1" if nodes[ni][0] in children else "0" for ni in xrange(nnodes))

  ## Nodes cannot overlap if they have the same parent
  parent = compute_parents(nodes)

  ## Output the upper-right non-overlap matrix
  for ni in xrange(nnodes):
    print " ".join("1" if ni < nj and parent[nodes[ni][0]] == parent[nodes[nj][0]] else "0" for nj in xrange(nnodes))

  ## Compute the ideal distance between nodes
  ideal = compute_ideal(nodes, dists, dist_model)
  
  ## Print the ideal distance matrix
  for (node, _, _) in nodes:
    print " ".join(str(ideal[(node, nodes[nj][0])]) if (node, nodes[nj][0]) in ideal else "0" for nj in xrange(nnodes))
  
    ## Print the weight matrix
  ## Placeholder
  for ni in xrange(nnodes):
    print " ".join("1" for nj in xrange(nnodes))

  if (len(lefts) > 0):
    grid = compute_grid(nodes, lefts)
    for (node, _, _) in nodes:
      print " ".join("1" if (node, nodes[nj][0]) in grid else "0" for nj in xrange(nnodes))

  if (len(aboves) > 0):
    grid = compute_grid(nodes, aboves)
    for (node, _, _) in nodes:
      print " ".join("1" if (node, nodes[nj][0]) in grid else "0" for nj in xrange(nnodes))



