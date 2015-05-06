This problem is all about computing properties of a graph (of friendships) and
scoring each node according to these properties.

Let’s look at the properties one by one.

7 points if G likes naughty, dirty games. This can be computed in O(1) for each node.

3 points for every friend of G who likes super hero figures. As we are registering a friendship (edge in the graph),
we just need to update the count of friends of a girl who like super hero figures. O(1) for each edge when building 
the graph, and O(1) when computing the score of each node (improved from the naive search of friends which could be
O(N)).

6 points for every friend of a friend of G, not including friends of G and G herself, who like men in leisure suits.
When registering friendships, we keep a set for each girl S(G) of her friends who like men in leisure suits. In order to
compute this score for a girl G, we iterate over every friend of hers G’ and compute the union of all S(G’) and then remove
G and her friends from this set to get the final result. This is more efficient than trying to compute this quantity from
scratch for each girl.

4 points if G has a friend H who likes cats and no friend of H (except perhaps G) likes cats.
For each girl, we keep a value V(G) that defines whether this girl has a friend who likes cats (and if so this is
the id of that node), if she doesn’t have a friend who likes cats (-1), or if she has more than one friend
who likes cats (-2). For each girl, this condition is satisfied iff V(G) >= 0 and (V(V(G)) == -1 or V(V(G)) == G). This
is computed in O(1), again more efficient than just doing it naively.

An important point to ensure the correctness of the solution is that we never register a friendship more than once as the
input will contain repeated friendships.
