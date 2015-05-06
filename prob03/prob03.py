primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
NUM_PRIMES = len(primes) #yeah, 25

def decompose(v, primes):
    p = 0
    counts = [0 for i in xrange(NUM_PRIMES)]
    while v > 1 and p < NUM_PRIMES:
        while v % primes[p] == 0:
            v /= primes[p]
            counts[p] += 1
        p += 1
    return counts

cum_counts = [[0 for i in xrange(NUM_PRIMES)]]

# open the file extracted from the xz archive
# and compute the how many times each prime is used
with open("numbers.txt") as f:
    lines = f.readlines()
    for line in lines:
        counts = decompose(long(line), primes)
        cum_counts.append([counts[i] + cum_counts[-1][i] for i in xrange(NUM_PRIMES)])

# returns a tuple of the count of the most frequent prime(s) in the interval [A,B)
# and a list of the prime(s) that have this count
def solve(A, B, cum_counts, primes):
    p_counts = [cum_counts[B][i] - cum_counts[A][i] for i in xrange(NUM_PRIMES)]
    max_p = max(p_counts)
    return (max_p, [primes[p] for p in xrange(NUM_PRIMES) if p_counts[p] == max_p])

T = int(raw_input())
for case in xrange(T):
    A, B = map(int, raw_input().split())
    max_p, ps = solve(A, B, cum_counts, primes)
    print max_p, ' '.join(map(str, ps))
