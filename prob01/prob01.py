def solve(N):
    return (N+1)/2

T = int(raw_input())
for case in xrange(T):
    N = int(raw_input())
    print solve(N)
