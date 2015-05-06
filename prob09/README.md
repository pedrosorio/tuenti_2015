The general idea is that you can precompute cumulative counts of the signals and
the signals squared and these can be used to obtain the mean and standard deviation of any
window of the signals in O(1).

Furthermore, you can precompute cumulative counts of wave[i]*pattern[i+d] for
each d (this must include negative d’s as well) in order to compute the cross correlation of a window
of the wave with the pattern at any given delay in O(1).

I would write down the actual algebraic manipulations to achieve these results but they are fairly trivial
and markdown doesn’t support LaTeX, so... do them yourself :P

This transforms the overall complexity of the code from O(N^4) to O(N^3).

The C++ code includes all of the original code used to compute the score (which you can ignore), and the
functions I implemented.
