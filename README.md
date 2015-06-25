# HqUcGl-of-Grouped-Networks
MIP, CP, SAT, MIP-LNS models corresponding to the declarative node placement discussed in the paper.
The CP model can be directly evaluated using any of the solvers supporting MiniZinc, including the G12 CPX constraint programming solver.
The MIP model can be evaluated using G12 MIP, CPLEX, or any other supporting solver.
The SAT model can be evaluated using the BumbleBEE solver.
The MIP-LNS model can be evaluated using CPLEX.

We include these to highlight how little "code" is required to reproduce the layouts in the paper using modern constraint programming languages.

The CP model (HqUcGl-cp.mzn) accepts input in minizinc data format (.dzn)
The MIP model (HqUcGl-mip.mod) accepts input in .dat data files.

The SAT model accepts input in .mod data files, which can be translated from a .mzn file using the mznout2mod.py 
the .mzn file is pretty simple to generate with the following format:
		#modules=
		1: [1]
		2: [2]
		3: [3]
		4: [1,2]
		#edges=
		(1,2)
		(3,4)
Then the gridlay2dense.py takes the .mod file as input and produces a .dense file as output,
Then the dense2bee.py takes the .dense file as input and produces a .bee file as output,
then the .bee file is solved using the BumbleBEE solver.

![alt tag](https://github.com/Vahany/HqUcGl-of-Grouped-Networks/tree/master/images/composers.png)

