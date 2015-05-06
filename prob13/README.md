Since we are using CFB mode and the key and iv are re-used every time, a plaintext with the same first x bytes as the
correct text should create a cipher with the same first x bytes as the cipher given as input in this problem.

Knowing this, we just need to generate a string that starts with 16 bytes defined by the server and whose sha1 last byte
is \xFF. Iterating over all 24 byte sequences that start with the correct prefix should take ~128 tries on average, so
testing new sequences is relatively fast.

There were two approaches to the brute force:
1) Use parallelism to split the search space of a single character (instead of having a single thread sequentially test
   all bytes from 32 to 127, use 8 threads to test 12 byte values each);
2) Use a dictionary to guess the next character in the message;
3) Use the NLP engine embedded in a human’s brain to predict the next character.

Obviously, 3rd is the most fun for the human being, so that’s the approach used in the code.
