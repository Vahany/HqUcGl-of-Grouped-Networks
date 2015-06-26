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

The following are examples of graph layouts produced by the models:
![alt tag](https://raw.githubusercontent.com/Vahany/HqUcGl-of-Grouped-Networks/master/images/composers.PNG)
"links between major composers, arranged with our model with the solver choosing the best orientation (vertical / horizontal) for nodes. Layout took 37.422 seconds using the SAT solver - disjunctions due to variable node orientation expand the search space."

![alt tag](https://raw.githubusercontent.com/Vahany/HqUcGl-of-Grouped-Networks/master/images/state_machine.PNG)
"Here is the same state-machine shown using our ultra-compact grid-based layout which has grid dimensions 4x4 leaving only three empty grid-cells.  This optimally compact solution was found in 0.464 seconds using the SAT solver.  Although we do not explicitly minimise bends or crossings, our layout is equal to the TSM output in these respects and significantly reduces the overall area and edge-length.  With the additional node area we are able to include more detailed descriptions of each state."

![alt tag](https://raw.githubusercontent.com/Vahany/HqUcGl-of-Grouped-Networks/master/images/tetris_bug.PNG)
"An example software-dependency graph with routing detail and the final result. Solved in 0.732 seconds with the SAT solver.  This network shows dependencies between types, methods and properties in C# code and was obtained in a debugging scenario using the Visual Studio Code Map tool. This layout neatly illustrates the cause of the bug: that Square is the only sub-class of Figure not created by the GetNextFigure method.  Code snippets and icons on each of the nodes give added context."

![alt tag](https://raw.githubusercontent.com/Vahany/HqUcGl-of-Grouped-Networks/master/images/les_mis_fd.PNG)
![alt tag](https://raw.githubusercontent.com/Vahany/HqUcGl-of-Grouped-Networks/master/images/les_mis_fdgs.PNG)
![alt tag](https://raw.githubusercontent.com/Vahany/HqUcGl-of-Grouped-Networks/master/images/les_miserables_lns.PNG)
The characters from Les-Miserables represented as nodes. Characters that appear in the same scene are connected. Took CPLEX with LNS 473.61 seconds to solve it. The colouring is based on communities.

