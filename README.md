# HqUcGl-of-Grouped-Networks
MIP, CP and SAT models corresponding to the declarative node placement given in section 3 of the paper.
The CP model can be directly evaluated using any of the solvers supporting MiniZinc, including the G12 CPX constraint programming solver.
The MIP model can be evaluated using G12 MIP, CPLEX, or any other supporting solver.
The SAT model can be evaliuated using the BumbleBEE solver.

We include these to highlight how little "code" is required to reproduce the layouts in the paper using modern constraint programming languages.
