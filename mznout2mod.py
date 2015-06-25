#!/usr/bin/python
import sys

(MODULE, EDGE, LEFT, ABOVE, DROP) = (0, 1, 2, 3, 4)

def tree_str(children, root, modnames):
  tstr = '(' + modnames[root] + ' '

  if len(children[root]) == 0:
    ## Leaf node
    tstr += '[1 1]'
  else:
    tstr += ' '.join([tree_str(children, child, modnames) for child in children[root]])
  tstr += ')'

  return tstr

def print_tree(children, roots, modnames):
  if len(roots) == 1:
    print tree_str(children, root, modnames)
  else:
    print '(root ' + ' '.join([tree_str(children, r, modnames) for r in roots]) + ')'

if __name__ == "__main__":
  prev = None
  modules = {}
  edges = []
  lefts = []
  aboves = []

  infile = sys.stdin

  mode = DROP

  for line in infile.readlines():
    line = line.strip()

    if line.startswith('#'):
      # Switch mode.
      if line.startswith('#modules'):
        mode = MODULE
      elif line.startswith('#edges'):
        mode = EDGE
      elif line.startswith('#left'):
        mode = LEFT
      elif line.startswith('#above'):
        mode = ABOVE
      else:
        mode = DROP
    elif line.startswith('----'):
      ## End of solution marker
      prev = (modules, edges)
      modules = {}
      edges = []
    elif line.startswith('===='):
      break
    else:
      if mode == MODULE:
        (mid, mstr) = line.split(': ')
        modules[int(mid)] = eval(mstr)
      elif mode == EDGE:
        edges.append(eval(line))
      elif mode == LEFT:
        lefts.append(eval(line))
      elif mode == ABOVE:
        aboves.append(eval(line))
      
  if len(modules) > 0 or len(edges) > 0:
    prev = (modules, edges)

  if prev is not None:
    (modules, edges) = prev

    leaves = set()
    for mod in modules:
      leaves.update(set(modules[mod]))

    ## Compute the tree of modules
    roots = []
    parents = {}
    children = { mod : [] for mod in modules }
    for mod in modules:
      modset = set(modules[mod])
      ancestors = [ m for m in modules if len(modules[m]) > len(modset) and modset.issubset(set(modules[m])) ]
      if len(ancestors) > 0:
        parent = min(ancestors, key=(lambda m : len(modules[m])))
        parents[mod] = parent
        children[parent].append(mod)
      else:
        parents[mod] = None
        roots.append(mod)
    #print modules 
    ## Pick names for the modules
    modnames = {}
    nmods = 0
    for mod in modules:
      if len(modules[mod]) == 1:
        modnames[mod] = "v{0}".format(modules[mod][0])
      else:
        modnames[mod] = "p{0}".format(nmods)
        nmods += 1

    print_tree(children, roots, modnames)

    print '#edges'
    for (s, d) in edges:
      print modnames[s], modnames[d], 1
    print '#left'
    for (s, d) in lefts:
      print modnames[s], modnames[d]
    print '#above'
    for (s, d) in aboves:
      print modnames[s], modnames[d]
