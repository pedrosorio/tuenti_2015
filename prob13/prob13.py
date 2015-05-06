import hashlib
import base64
import Crypto.Cipher
import socket
import string

with open("input.txt") as f:
    b64encoded = f.readline().strip()
    binary_data = base64.b64decode(b64encoded)

cryp = [ord(c) for c in binary_data]

def encrypt(message):
    return base64.b64encode(Crypto.Cipher.AES.new(pk, Crypto.Cipher.AES.MODE_CFB, iv).encrypt(message))

last = [chr(i)+chr(j) for i in xrange(256) for j in xrange(256)]

def get_sha1(s):
    h = hashlib.new('sha1')
    h.update(s)
    return h.digest()

def get_proof(prefix):
    med = prefix + '000000'
    i = 0
    while get_sha1(med+last[i])[-1] != '\xff':
        i += 1
    return med+last[i]

# check whether the msg hashes to the same bytes as the received cypher text
def check_message(msg):
    TCP_IP = "54.83.207.93"
    TCP_PORT = 12345
    PROOF_START_LEN = len("Send a string starting with ")
    PREFIX_LEN = 16
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    proof_request = s.recv(200)
    prefix = proof_request[PROOF_START_LEN:PROOF_START_LEN+PREFIX_LEN]
    proof = get_proof(prefix)
    s.send(proof)
    IS_OK = s.recv(100)
    s.send(msg)
    enc = s.recv(2000)
    binary_enc = base64.b64decode(enc)
    return binary_enc[len(msg)-1] == binary_data[len(msg)-1]


# Yeah, I could have brute forced this using multiple threads to make the search faster
# But I was kind of brain dead so I did an "interactive program" that asks the user
# to guess the next character and searches that one first.
# After that, brute force goes through space and lowercase chars first as they are the
# most common so we search them first if the user is not sure
chars_test = " " + string.lowercase + string.uppercase
extra = ''.join([chr(c) for c in xrange(256) if chr(c) not in chars_test])
chars_test += extra

message = ""
for i in xrange(len(message),len(cryp)):
    print len(message), message
    # ask the user to guess
    done = False
    while not(done):
        print "next char:"
        c = raw_input()
        if c:
            if check_message(message + c):
                message += c
                done = True
        else:
            break
    if done:
        continue
    # brute force if the user has no good ideas
    for c in chars_test:
        if check_message(message + c):
            message += c
            break

# print complete message
print message
