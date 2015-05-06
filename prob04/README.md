This one required a couple of tries to figure out the order of operations
and the final solution is straightforward:

- First, decode the base64 into a string of 0’s and 1’s (easiest for the purposes of fetching n bits,
  but if memory had been a concern, it would have been equally easy to use the raw representation)
- For each instruction, parse it, read n bits and then:
    *  If it should be little endian, reverse the order of the bytes (“partial bytes” get copied as is,
       so 5 bits at the end of the sequence get copied to the beginning with no trailing 0 bits)
    *  If it should be reversed, just reverse the bit string
    *  Convert it to a long integer and print
