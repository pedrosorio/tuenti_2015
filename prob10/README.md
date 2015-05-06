This one is awesome. Whenever a user tries to login, the server checks if the user and password
and exist in a table of a given database (storing password in plaintext ftw :D).

The server has a configuration file that contains the parameters to connect to the database, but this
file is only read once when the user connects to the page. After that, the server sets two cookies:
- One contains the configuration parameters of the server (config)
- The other contains an md5 hash of a server variable “secret” + config

After these cookies are set, the server uses the config in the user cookie to connect to the database.
It becomes clear that we need to change the config cookie to make the server connect to a db that we own
containing the user/password combination we choose.

The problem is the server checks if the sig cookie has the correct value. In order to obtain the sig cookie we
need to know the value of the “secret” variable to salt our config before computing the md5 hash. 
We see that secret is read from the second field of the first line in /etc/passwd. The hint is helpful and it’s
basically telling us that no one stores passwords in /etc/passwd anymore and looking at a file in a linux system
one can see the second field is always “x”.

Now all we have to do is create our db, with a users table and a dummy user and password. Next, create the config,
create the sig as md5(“x”+config), set the cookies and send a post request with the dummy user and password, and we
get our [prize](https://www.youtube.com/watch?v=Sagg08DrO5U) :)
