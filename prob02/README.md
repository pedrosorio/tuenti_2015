Every (ordered) pair of primes defines a unique approximate
prime as a result of the [fundamental theorem of arithmetic](http://en.wikipedia.org/wiki/Fundamental_theorem_of_arithmetic).

Since we know the maximum approximate prime we will need to compute is 10**8,
the maximum prime is <= 10**8/2. We can use the efficient [Sieve of Erathosthenes](http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)
to compute this list of primes.

We then multiply all the pairs of primes (skipping most combinations that are > 10**8),
which is pretty fast as there are only 17.427.258 approximate primes in the range.

After that, we sort the approximate primes and to answer each query binary search
the A and B and return the difference between their positions in the sorted array.
