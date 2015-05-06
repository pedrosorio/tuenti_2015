from pulp import * # http://pythonhosted.org//PuLP/index.html

fo = open("file_out.txt", "w")

def solve(T, S, P, M, K):
    #start the definition of the lp problem
    pb= LpProblem("prob", LpMinimize)
    #define the lp variables (i.e. time spent by each person on each tree)
    lp_vars = [[] for p in xrange(P)]
    for p in xrange(P):
        for t in xrange(T):
            lp_vars[p].append(LpVariable("x"+str(p)+"_"+str(t), 0, min(K[p][t], M[p])))
    #define the objective (minimize sum of time spent)
    pb += lpSum([lp_vars[p][t] for p in xrange(P) for t in xrange(T)])
    #define the constraints
    for p in xrange(P): # each person may only spend M[p] minutes at most
        pb += lpSum([lp_vars[p][t] for t in xrange(T)]) <= M[p]
    for t in xrange(T): # each tree must be completely cut down
        pb += lpSum([lp_vars[p][t] * 1.0/K[p][t] for p in xrange(P)]) == 1
    GLPK().solve(pb)
    # The following for debugging purposes (there was no bug, just forgot to format to 2 decimal places :P)
    for t in xrange(T):
        print "Tree {}:".format(t)
        print " ".join([str(lp_vars[p][t].varValue) for p in xrange(P)]) + " -> " + str(sum([lp_vars[p][t].varValue *1.0/K[p][t] for p in xrange(P)]))
    for p in xrange(P):
        print "Person {}:".format(p)
        print " ".join([str(lp_vars[p][t].varValue) for t in xrange(T)]) + " -> " + str(sum([lp_vars[p][t].varValue for t in xrange(T)])) + "({})".format(M[p])
    return value(pb.objective)

E = int(raw_input())
for case in xrange(1,E+1):
    T, S, P = map(int, raw_input().split())
    M, K = [], []
    for person in xrange(P):
        vals = map(int, raw_input().split())
        M.append(vals[0])
        K.append(vals[1:])
    sol = solve(T, S, P, M, K)
    print sol
    if (sol == 0):
        sol = "IMPOSSIBLE"
    elif S >= sol:
        sol = "RIGHT"
    else:
        sol = "{0:.2f}".format(sol - S)
    fo.writelines("Test case #{}: {}\n".format(case, sol))
fo.close()
