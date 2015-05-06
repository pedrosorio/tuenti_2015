#!/usr/bin/env python

import random
import sys
import argparse

MIN_VALUE=1
MAX_VALUE=10000

def main(M, N, filename):
    with open(filename, 'wb') as f:
        f.write('%d %d\n' % (M, N))
        for _ in xrange(M):
            vals = [str(random.randint(MIN_VALUE, MAX_VALUE)) for _ in xrange(N)]
            f.write('%s\n' % (' '.join(vals)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Generate the sheet matrix')
    parser.add_argument(
            '--N', type=int, default=5000,
            help='Length of the matrix in axis X')
    parser.add_argument(
            '--M', type=int, default=5000,
            help='Length of the matrix in axis Y')
    parser.add_argument(
            '--seed', type=int, default=13371337,
            help='Seed for random numbers')
    parser.add_argument(
            '--filename',
            option_strings=['--file','--f'], metavar='filename', type=str,
            default='sheet.data', help='Filename for the sheet data')

    args = parser.parse_args()
    random.seed(args.seed)
    N = args.N
    M = args.M 
    main(M, N, args.filename)

