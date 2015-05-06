At first I tried to model the problem as a min cost max flow on a graph with people and trees but since the limits
are very low and it is clearly a linear program, we can just use any library that contains a linear programming solver
and be done with it. An optimized solver such as GLPK solves the provided instances in a fraction of a second.
