Given the problem description we can define a directed graph where:
1) Each node corresponds to one enemy ship
2) The ships inside the explosion range of some ship have incoming edges from this ship

When we pick a node in the graph (a ship), the set of reachable nodes correspond to the ships that
will be destroyed in the chain reaction. We want to find the minimal set of nodes we need to pick to
reach all of them.

It is evident that we need to pick all the sources (nodes that don’t have incoming edges) because they will
never be affected by a chain reaction. It is not sufficient to pick the sources of the graph because we may
have cycles. For example, ships 1,2,3 are in a cycle where 1->2->3->1 and they are not in the explosion area
of any other ship therefore we must pick at least one of them or they won’t explode; however, since they all
have incoming edges, they are not sources in the graph.

A good way to solve this problem is to compute the condensed graph. This a DAG where each
node replaces a [strongly connected component](http://en.wikipedia.org/wiki/Strongly_connected_component)
in the original graph, and the edges between the nodes are the ones that exist between different SCC in the
original graph (where repeating edges can be ignored).

In order to cover the condensed graph, it is sufficient and necessary to pick its sources (because it is a DAG).
Furthermore, in the original graph, if we pick a node inside an SCC, by definition all of the nodes in that SCC are
reachable. This implies that picking a single node for each SCC that is a source in the condensed graph is sufficient
and necessary to cover the entire graph.

In terms of implementation we need to do 2 things:
1) Define the original graph by iterating over all ships and checking if they are inside the polygon defined by
   each ship (this is O(N^2) and can’t be made better in the worst case, but in practice if most polygons are relatively
   small compared to the full “map” we can bucketize the location of the ships  and only consider those ships that are 
   inside the rectangle that encloses the polygon).
2) Compute the condensed graph and count its sources - in this case we can use the Tarjan algorithm to find the SCCs
   and determine if there are any incoming edges to each SCC.
