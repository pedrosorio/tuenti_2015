import heapq

N = int(raw_input())
node_dict = {}
node_cost = []
goal_node = 0
for i in xrange(N):
    name, cost = raw_input().split()
    if name == "Raftel":
        goal_node = i
    node_cost.append(int(cost))
    node_dict[name] = i

routes = [[] for i in xrange(N)]
R = int(raw_input())
for i in xrange(R):
    name1, name2, cost = raw_input().split()
    n1 = node_dict[name1]
    n2 = node_dict[name2]
    routes[n1].append((n2, int(cost)))

S = int(raw_input())
ships = []
for i in xrange(S):
    number, name, gold, start = raw_input().split()
    ships.append((int(number), name, int(gold), node_dict[start]))

# Here assuming all ships have a greater number than our ship (i.e. they move later)
my_ship = ships[0]
ships = {ship[0]:ship[1:] for ship in ships[1:]}

# returns the next node visited by an enemy pirate ship
def get_next_node(cur_node, num, routes, visited):
    m_cost = -1
    go_to = cur_node
    for nnode, cost in routes[cur_node]:
        if nnode not in visited:
            if m_cost == -1 or (num%2 == 0 and cost > m_cost) or (num%2 == 1 and cost < m_cost):
                go_to = nnode
                m_cost = cost
    return go_to

# extra cost to visit node j at time i (because pirate ships will reach it when we're there)
extra_cost = [[0 for j in xrange(N)] for i in xrange(N)]
mn_time_to_goal = N
for num, ship in ships.iteritems():
    name, gold, cur_node = ship
    visited = set([cur_node])
    time = 0
    while cur_node != goal_node:
        extra_cost[time][cur_node] += gold
        next_node = get_next_node(cur_node, num, routes, visited)
        if next_node == cur_node:
            break
        time += 1
        visited.add(next_node)
        cur_node = next_node
    if cur_node == goal_node:
        mn_time_to_goal = min(mn_time_to_goal,time)

# remove times > mn_time_to_goal because our ship must reach before this time
extra_cost  = extra_cost[:mn_time_to_goal+1]

# compute upper bound on the maximum gold that can be obtained if we are at node j
# and i turns have passed, for routes that reach the goal before any other pirate
# from node j before reaching the goal
# upper bound because it ignores restrictions to visit an island twice
upper_bound = [[None if j != goal_node else 0 for j in xrange(N)] for i in xrange(mn_time_to_goal+1)]
for time in xrange(mn_time_to_goal-1, -1, -1):
    for node in xrange(N):
        if node != goal_node and upper_bound[time+1][node] is not None:
            upper_bound[time][node] = upper_bound[time+1][node] + 10
        for pnode, cost in routes[node]:
            if upper_bound[time+1][pnode] is not None:
                travel_cost = node_cost[pnode] + cost
                pirate_cost = extra_cost[time+1][pnode]
                potential_gold = upper_bound[time+1][pnode] - pirate_cost - travel_cost
                if upper_bound[time][node] is None or upper_bound[time][node] < potential_gold:
                    upper_bound[time][node] = potential_gold

cur_node = my_ship[3]
my_gold = my_ship[2]
cur_time = 0
visited = set([cur_node])
states = [(-(my_gold + upper_bound[cur_time][cur_node]), cur_time, cur_node, my_gold, visited)]
max_gold = -1000000000000
while True:
    upper, cur_time, cur_node, my_gold, visited = heapq.heappop(states)
    # negative because it is a min_heap and we want to visit nodes with largest
    # upper bound first
    upper = -upper
    if upper <= max_gold:
        break
    if my_gold > 0:
        for nnode, cost in routes[cur_node]:
            next_upper = upper_bound[cur_time+1][nnode]
            if nnode in visited or next_upper is None:
                continue
            travel_cost = node_cost[nnode] + cost
            pirate_cost = extra_cost[cur_time+1][nnode]
            total_cost = travel_cost + pirate_cost
            next_gold = my_gold - total_cost
            if nnode == goal_node:
                max_gold = max(max_gold, next_gold)
                continue
            next_upper += next_gold
            if next_upper <= max_gold:
                continue
            next_visited = visited.copy()
            next_visited.add(nnode)
            heapq.heappush(states, (-next_upper, cur_time+1, nnode, next_gold, next_visited))
    next_upper = upper_bound[cur_time+1][cur_node]
    if next_upper is None:
        continue
    next_gold = my_gold + 10 - extra_cost[cur_time+1][cur_node]
    next_upper += next_gold
    if next_upper <= max_gold:
        continue
    heapq.heappush(states, (-next_upper, cur_time+1, cur_node, next_gold, visited))

print max_gold
