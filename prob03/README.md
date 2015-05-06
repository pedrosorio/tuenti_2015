In this problem we are given a list of very large numbers and need to find the most common prime factors
within a specific sublist of those numbers.

The obvious solution involves pre-computing some things in the number list:
 - First, factorizing the numbers into their prime factors (which is easy in python)
 - Second, keep a cumulative count of how many times a prime factor appears for numbers 1..n in the list

To answer a query:
 - Find the total number of times each prime appears in a..b by subtracting the cumulative counts at b and a-1
 - Find the most common one(s) and print it/them
