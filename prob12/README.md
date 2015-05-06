Another great problem. Possibly my favorite this year.

The first natural step is to try to use the terminal to do stuff. The first command that needs to be executed is
reqant to request access to the antena. Using the developer tools in the browser we can find the OS.user and OS.password
required to make the command work.

Then we need to use the photocmd with code we received from the previous command. The problem is, this one never finishes :(

Inspecting the code for the forth interpreter, there is a limit of 1000 characters that can be processed before a new interval
is set for the command to wait again. Even after removing this, it’s still too slow, so we go ahead and dive into the forth code.

After learning forth to understand what those functions are doing, it turns out there are some pretty inefficient
things going on. The best examples are the A and S functions that just add and subtract but do so by executing a for
loop (lol).

Fixing this allows the function to finish quickly and we can use the photoview function with the received filename.
Sure enough, the image is impossible to understand, seems like a lot of random noise is present. Restarting the terminal
we re-do the process and compare the images (see the 2 images in the images/ folder). They are visually similar but not
identical. It looks like the “solar flare” is super-imposing some random noise on a “good” image. If you have ever done 
any kind of signal processing, what you have to do next is obvious - get a bunch of images and average the noise out.

Now, at this point the smart thing to do would have been to  automate the process in javascript in a simple way (create a separate
file, call the functions repeatedly getting the results from the DOM, average the resulting images).

Instead, I decided to define more primitives in the forth interpreter that append the value in the forth stack to a javascript
variable which gets returned when execution finishes.

I wrote a function in the terminal.js script that obtains the urls of 50 different pictures (by ensuring the datetime is
different) and places them in a variable. These are then copied to the urls.txt file (in images dir) and we can run:
cat urls.txt | xargs -n 1 curl -O

to obtain the 50 images. After this, just run get_average.py to get an averaged image (Average.png) and notice the QR code.
The code contains the key required to submit the problem.
