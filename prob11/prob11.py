import sys

# This should have been a trivial dp, but somehow it ended up in this
# slow stupid mess

sys.setrecursionlimit(5000)

MOD = 1000000007
MAX_DOORS_DOWN = 400

# compute binomial coefficients % MOD
bnm = [[1]]
for i in xrange(1,MAX_DOORS_DOWN+1):
    bnm.append([1] + [(bnm[i-1][j] + bnm[i-1][j+1]) % MOD for j in xrange(i-1)] + [1])

scenarios = []
mx = 0
with open("scenarios.txt") as f:
    N = int(f.readline())
    for sc in xrange(N):
        S, R = map(int, f.readline().strip().split())
        room_id = {}
        rooms = []
        for room in xrange(R):
            name, d = f.readline().strip().split()
            room_id[name] = room
            d = int(d)
            room_doors = []
            for door in xrange(d):
                y, k, s = f.readline().strip().split()
                room_doors.append([y, int(k), int(s)])
            rooms.append([room_doors,[]])
        # add "exit" room
        room_id["exit"] = R
        rooms.append([[],[]])
        # replace room names with ids in the description of the doors
        # populate an array for each room with the list of rooms that
        # have doors going down to it and the keys required to open each
        # door and the stamina required  to go down the stairs
        for room in xrange(R+1):
            room_doors = rooms[room][0]
            #if sc == 9:
                #print room, len(room_doors)
            for door in room_doors:
                door[0] = room_id[door[0]]
                #if sc == 9:
                    #print door
                rooms[door[0]][1].append([room, door[1], door[2]])
        scenarios.append([rooms, S])

def get_dp(dp, room, stamina, rooms, bnm, max_stamina):
    if dp[room][stamina] != -1:
        return dp[room][stamina]
    up_doors = rooms[room][1]
    total = 0
    for up_room, door_keys, door_stamina in up_doors:
        up_room_num_doors = len(rooms[up_room][0])
        if door_keys > up_room_num_doors:
            continue
        if stamina == max_stamina and door_stamina < 0:
            up_stamina_range = xrange(max(0, max_stamina + door_stamina), max_stamina+1)
        else:
            up_stamina_range = [stamina + door_stamina]
        for up_stamina in up_stamina_range:
            if up_stamina > max_stamina or up_stamina < 1:
                #print room, stamina, up_room, up_stamina, max_stamina
                continue
            if stamina == 0:
                # special case where the hero had to kill minions to get just enough stamina
                for minions_killed in xrange(max(1, door_keys), min(up_room_num_doors, up_stamina)+1):
                    if up_stamina == max_stamina:
                        if minions_killed > max(1, door_keys):
                            initial_stamina_range = [max_stamina-minions_killed]
                        else:
                            initial_stamina_range = xrange(max_stamina-minions_killed, max_stamina+1)
                    else:
                        initial_stamina_range = [up_stamina-minions_killed]
                    for initial_stamina in initial_stamina_range:
                        total = (total + (bnm[up_room_num_doors-1][minions_killed-1] * get_dp(dp, up_room, initial_stamina, rooms, bnm, max_stamina))) % MOD
            else:
                # the hero came down from a room after picking up enough keys
                minions_killed = max(1, door_keys)
                if up_stamina - minions_killed < 0:
                    continue
                if up_stamina == max_stamina:
                    initial_stamina_range = xrange(up_stamina-minions_killed, max_stamina+1)
                else:
                    initial_stamina_range = [up_stamina-minions_killed]
                for initial_stamina in initial_stamina_range:
                    total = (total + (bnm[up_room_num_doors-1][minions_killed-1] * get_dp(dp, up_room, initial_stamina, rooms, bnm, max_stamina))) % MOD
    dp[room][stamina] = total
    #print room, stamina, total
    return total


def solve(rooms, max_stamina):
    #print len(rooms), max_stamina
    R = len(rooms)
    S = max_stamina
    # number of ways to get to room i with stamina j % MOD | -1 before computing
    dp = [[-1 for j in xrange(S+1)] for i in xrange(R+1)]
    # the scenario description always starts with the "start" room
    for stamina in xrange(max_stamina):
        dp[0][stamina] = 0
    dp[0][S] = 1
    total = 0
    EXIT_ROOM = R-1
    for room in xrange(1, R-1):
        for stamina in xrange(S+1):
            get_dp(dp, room, stamina, rooms, bnm, S)
    for stamina in xrange(S+1):
        v = get_dp(dp, EXIT_ROOM, stamina, rooms, bnm, S)
        total = (total + v) % MOD
    return total


for s in map(int, sys.stdin.read().split()):
    print "Scenario {}: {}".format(s, solve(scenarios[s][0], scenarios[s][1]))

