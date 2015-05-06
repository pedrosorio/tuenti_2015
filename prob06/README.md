In this one we need to find the best airscrew, which is a couple of squares of side k diagonally joined
by an axis (empty) of size 1x1.

For a given sheet section and k value, we can try all possible placements of the axis which define an
airscrew, and compute the sum of values under the two squares to find the best placement.

The only challenge here is how to compute the sum of values in the squares efficiently and the problem
is just begging for us to use the concept of [integral image](http://en.wikipedia.org/wiki/Summed_area_table).

This means (yeah, you’ve got it) precomputation for the whole sheet in O(N*M), which will allow us to compute
the score of any square (or rectangle for that matter) in O(1).

