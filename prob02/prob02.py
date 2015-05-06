from math import sqrt
import bisect

MAX_RANGE = 10**8
MAX_PRIME = MAX_RANGE/2


# pre-compute primes that could generate approximate primes
# using the sieve of eratosthenes
is_prime = [True for i in xrange(MAX_PRIME+1)]
v = 2
while v * v <= MAX_PRIME:
    for i in xrange(2*v, MAX_PRIME+1, v):
        is_prime[i] = False
    v += 1
    while not is_prime[v]:
        v += 1

primes = [i for i in xrange(2, MAX_PRIME+1) if is_prime[i]]

# pre-compute the list of approximate primes by multiplying
# every pair of primes up until MAX_RANGE
approx = []

for i in xrange(len(primes)):
    for j in xrange(i, len(primes)):
        v= primes[i] * primes[j]
        if v > MAX_RANGE:
            break
        approx.append(v)

# sort the approximate primes such that the number of
# in the range [A,B] can be binary searched in O(log(MAX_RANGE))
#
# (alternatively we could keep the cumulative count of
# approximate primes at the cost of O(MAX_RANGE) memory
# allowing us to answer each query in O(1))
approx.sort()

def solve(approx, A, B):
  start = bisect.bisect_left(approx, A)
  end = bisect.bisect_right(approx, B) - 1
  return end-start+1

T = int(raw_input())
for case in xrange(T):
    A, B = map(int, raw_input().split())
    print solve(approx, A, B)

