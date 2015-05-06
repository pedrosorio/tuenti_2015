from base64 import b64decode
import string

# convert character to 8bit string
def char_to_8bit(char):
    return bin(ord(char))[2:].zfill(8)

# returns a string of bits representing the base64 encoded value
def decode_to_bits(base64string):
    return ''.join(map(char_to_8bit, b64decode(base64string)))

# convert bit string to little_endian format
def little_endian(bitstring):
    bytestart = range(0,len(bitstring),8)
    byte_list = [bitstring[b:b+8] for b in bytestart]
    return ''.join(byte_list[::-1])

# get number of bits, whether to use little endian
# and whether to reverse bits from instruction string
def get_instruction(inst):
    num_bits = int(''.join([c for c in inst if c in string.digits]))
    return (num_bits, 'L' in inst, 'R' in inst)

b64string = raw_input()
bits = decode_to_bits(b64string)
cur_bit = 0
N = int(raw_input())
for cpu in xrange(N):
    num_bits, l_endian, rev = get_instruction(raw_input())
    message = bits[cur_bit:cur_bit+num_bits]
    cur_bit += num_bits
    if l_endian:
        message = little_endian(message)
    if rev:
        message = message[::-1]
    print long(message, 2)
