In this problem we use Counter objects from the collections package which are
very useful to keep track of the inventory and easily figure out whether an element can be generated using
the current inventory.

First we parse the alchemy book to obtain a Counter() of the elements needed to generate each complex element.
We also maintain a reverse reference where each element contains has a list of all the complex elements it can
be used to create (i.e. the ones that use it directly as a source).

Given this information, we can start with our inventory and do a DFS on the graph of inventories that can be obtained by
generating combining elements from the current inventory.
Since every recipe reduces the number of elements in the inventory, this is guaranteed to have a base case.
Also, we never visit the same inventory state again because we keep a set of inventories that have been explored.
If we compute the amount of gold gained from selling the items of each inventory, the solution is the max of these.
