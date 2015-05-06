# DISCLAIMER: Yeah, yeah, ugliest code ever, I am pre-computing everything, since the limits on N
# and M are silly and give no indication of the actual algorithm efficiency required

# If you want me to implement an extensible engine that scores profiles in a social network
# don't do it in a contest, pay me for it instead :P

N, M = map(int, raw_input().split())
name_to_id = {}
answers = []
for i in xrange(N):
    val = raw_input().split()
    name_to_id[val[0]] = i
    answers.append(val[1:])

# adjacency lists of the friend graph
friend_graph = [set([]) for i in xrange(N)]
# friend graph that only contains friends who like men in leisure suits
leisure_friend_graph = [set([]) for i in xrange(N)]
# number of friends of each girl who like superheros
friends_like_super_hero = [0 for i in xrange(N)]
# id of the friend of each girl who likes cats, -1 if no friend, -2 if more than one friend
friend_who_likes_cats = [-1 for i in xrange(N)]

def register_super_hero_info(g1, g2, answers, friends_like_super_hero):
    if answers[g1][1] == 'Y':
        friends_like_super_hero[g2] += 1

def register_cat_info(g1, g2, answers, friend_who_likes_cats):
    if answers[g1][3] == 'Y':
        if friend_who_likes_cats[g2] == -1:
            friend_who_likes_cats[g2] = g1
        else:
            friend_who_likes_cats[g2] = -2

def add_friendship(g1, g2, answers, friend_graph, leisure_friend_graph, friends_like_super_hero, friend_who_likes_cats):
    if g2 in friend_graph[g1]:
        return
    friend_graph[g1].add(g2)
    if answers[g2][2] == 'Y':
        leisure_friend_graph[g1].add(g2)
    register_super_hero_info(g1, g2, answers, friends_like_super_hero)
    register_cat_info(g1, g2, answers, friend_who_likes_cats)

for i in xrange(M):
    clique = [name_to_id[name] for name in raw_input().split()]
    for i in xrange(len(clique)):
        for j in xrange(len(clique)):
            if i == j:
                continue
            add_friendship(clique[i], clique[j], answers, friend_graph, leisure_friend_graph, friends_like_super_hero, friend_who_likes_cats)

# find connected components using dfs
connected_component = [0 for i in xrange(N)]
comp = 1
girl = 0
while girl < N:
    if connected_component[girl] == 0:
        connected_component[girl] = comp
        stack = [girl]
        while stack:
            g = stack.pop()
            connected_component[g] = comp
            for friend in friend_graph[g]:
                if connected_component[friend] == 0:
                    connected_component[friend] = comp
                    stack.append(friend)
        comp += 1
    girl += 1

# pre-compute how many girls like shopping in each connected component
comp_like_shopping = [0 for i in xrange(comp)]
for girl in xrange(N):
    if answers[girl][4] == 'Y':
        comp_like_shopping[connected_component[girl]] += 1
total_like_shopping = sum(comp_like_shopping)

def get_num_friends_of_friends_who_like_leisure_suits(girl, friend_graph, leisure_friend_graph):
    friends = friend_graph[girl]
    friends_of_friends = set([])
    for friend in friends:
        friends_of_friends |= leisure_friend_graph[friend]
    # remove friends and the girl herself from friends of friends
    friends_of_friends -= (friends | set([girl]))
    return len(friends_of_friends)

# compute the score for each girl
max_score = 0
for girl in xrange(N):
    score = 0
    if answers[girl][0] == 'Y':
        score += 7
    score += 3 * friends_like_super_hero[girl]
    score += 6 * get_num_friends_of_friends_who_like_leisure_suits(girl, friend_graph, leisure_friend_graph)
    if friend_who_likes_cats[girl] >= 0:
        friend = friend_who_likes_cats[girl]
        if friend_who_likes_cats[friend] == -1 or friend_who_likes_cats[friend] == girl:
            score += 4
    component = connected_component[girl]
    score += 5 * (total_like_shopping - comp_like_shopping[component])
    max_score = max(max_score, score)

print max_score
