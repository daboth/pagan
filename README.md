pagan
=====

Welcome to the Python Avatar Generator for Absolute Nerds.

**Current version: 0.4.3**

View the change history [here](CHANGELOG.md).

Remember those good old days when your imagination was a big part of the
computer gaming experience? Hardware limitations forced you to fill the void
left by poorly pixelated images. Pagan brings back those nostalgic feelings
by generating **identicons** in an old-school style inspired by retro
roleplaying adventure games.

Pagan hashes input strings to generate unique avatar images intended for use as
profile pictures in web applications. These images can be used to replace
default user images for new accounts, or to enhance comment sections by visually
representing a user's IP address or username.

**Pagan is currently under development. It can perform the following functions:**

* Generate identicons with unique colors and gear based on any input string.
* Use multiple hash functions from within Python's hashlib.
* Create avatar images to fit a specific resolution.
* Remap 16x16 generated pixelmaps to a required image size.
* Expand generated pagans by adding new weapons or gear.

Enjoy the nostalgia!

### Some example avatars hashed with SHA512:

Input  | Avatar
------------- | -------------
pagan  | ![pagan](/images/pagan.png)
python | ![python](/images/python.png)
avatar | ![avatar](/images/avatar.png)
github | ![github](/images/github.png)
retro | ![retro](/images/retro.png)
piece of cake | ![piece of cake](/images/piece%20of%20cake.png)
hash me if you can | ![hash me if you can](/images/hash%20me%20if%20you%20can.png)

### Installation:

To install Pagan, first clone this repository:
```
>> git clone https://github.com/daboth/pagan.git
```
Then, enter this command at the terminal to manually install Pagan:
```
>> python setup.py install
```
Alternatively, use this command to install pagan via pip:
```
>> pip install pagan
```

### Python usage example:
```python
# Import the pagan module.
import pagan

# Acquire an arbitrary string.
inpt = 'pagan'

# Use pagan to generate an avatar object based on an input string.
# Optional: You may specify which hash function Pagan should use.
# The functions are available as constants.
# Default: MD5.
img = pagan.Avatar(inpt, pagan.SHA512)

# Open the avatar image in an
# external image viewer.
img.show()

# Set an output path and a file name.
# You don't need to specify a file ending.
# Choose a path depending on your OS.
outpath = 'output/'
filename = inpt

# Saves the avatar image as a .png file
# by omitting the path and name. The
# file endings will be generated automatically.
img.save(outpath, filename)

# You can change the avatar input and
# hash function anytime.
img.change('new input', pagan.SHA256)
```

### Command Line Interface

The pagan command line interface can be used to generate avatars without needing
to write a python script:
```
>> pagan [-h] [--show] [--output OUTPUT] [--hash HASH] input [input ...]
```

For example, typing
```
>> pagan hello
```
will generate an avatar from the string 'hello' and save it in the current
working directory.

For more information, execute Pagan using the *-h* help parameter:
```
>> pagan -h
```

### Webserver

A demo of Pagan can be run in a webserver application. To access the Pagan demo,
execute the following instructions from the webserver directory:
```
>> cd /tools/webserver/
>> python webserver.py
```
Beware: This demo of Pagan will fill your temporary directory with generated
image files. Do not run it in production!

The webserver will serve from localhost port 8080. Open this adress in your
browser window:
```
http://127.0.0.1:8080/
```

### Supported Hashes

Hash     | Constant
-------- | --------
md5 | pagan.MD5
sha1 | pagan.SHA1
sha224 | pagan.SHA224
sha256 | pagan.SHA256
sha384 | pagan.SHA384
sha512 | pagan.SHA512

### Testing

To test Pagan, you must install either the pytest or tox Python modules.
Configure tox.ini to test different Python versions.

### Docker

To use pagan within Docker, you must build the Docker image with:

```
>> docker build -t pagan .
```

Then, run docker image

```
>> docker run -d -p 8080:8080 -t pagan
```

The webserver inside Docker will serve from localhost port 8080. Open this adress in your
browser window:
```
http://127.0.0.1:8080/
```

If you want to use PAGAN CLI, you just have to look for the IP Adress of the Docker container and then connect through ssh with user: pagan and pass: pagan, like this:

```
>> ssh -X pagan@dockercontainerip
```


#### Using py.test

```
>> pip install pytest
>> pytest
```

#### Using tox

```
>> pip install tox
>> tox
```
