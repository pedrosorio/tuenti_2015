This is the first problem with a lengthy rule description so it’s good to clarify some aspects of it.

We are to travel through a graph without revisiting any node, and we need to find the path that reaches
a goal node before any other pirate ship does. Among these paths we have to find the one that gets there
with largest amount of gold.

*Precomputation*

The first observation we can make is that other pirate routes don’t depend on our moves, so we can precompute
them. In fact, the different pirate ships are not relevant. All we care about is the total amount of gold
in pirate ships that arrive at node i after j steps. This is the penalty we need to pay for a specific time
step (apart from the constant penalties/bonuses defined by the graph).

By computing the pirate routes, we also have another vital information - the time step j when the first pirate
ship arrives in Raftel. Any solution will have to ensure that we take j or fewer steps to reach it.

*More precomputation*

Another useful information is to have a good upper bound on the maximum amount of gold we can get in the future
assuming j steps have passed and we are at node i. This can be done by simple dynamic programming starting with
0 for any time step if we have reached Raftel (we can’t get more gold after that) and taking into account the
penalties from traversing edges / arriving at islands / pirates arriving after us.

*A-star*

Now, we just need to find the maximum gold we can get by arriving at Raftel before any other pirates. We keep
priority queue sorted by (current_gold + upper_bound_gold_we_could_get_in_the_future) and explore the graph.
If the top of the priority queue ever gets <= than the current optimum, we stop the search and return the result.
