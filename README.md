pagan
=====

Welcome to the Python avatar generator for absolute nerds.

**Current version: 0.4.3**

View changes [here](CHANGELOG.md).

Remember those good old days when your own imagination was a big part of the
computer gaming experience? All the limitations of the hardware forced you to
fill the void left by poorly pixelated images by yourself. Well, pagan tries to
give back some of those nostalgic feelings by providing **identicons** in an
oldschool look that are inspired from retro roleplaying adventure games.

Each string input will be hashed and a unique avatar image is generated. The purpose
of pagan is to use it for generating a user image in any web application. It is
is meant to replace default user images when creating new accounts or to enhance
comment sections, e.g. visualizing the author's IP address or username.

**The software is currently under development and features the following functions:**

* Process a given string to generate identicons with unique colors and gear.
* The hash function can be chosen from the ones included in Python's hashlib.
* Create the avatar image based on a given resolution.
* Pagan will map all virtual 16x16 pixels to the real image size.
* Expand pagan by adding new weapons or gear.
* Enjoy the nostalgia!

###Example avatars hashed with SHA512:

Input  | Avatar
------------- | -------------
pagan  | ![pagan](/images/pagan.png)
python | ![python](/images/python.png)
avatar | ![avatar](/images/avatar.png)
github | ![github](/images/github.png)
retro | ![retro](/images/retro.png)
piece of cake | ![piece of cake](/images/piece%20of%20cake.png)
hash me if you can | ![hash me if you can](/images/hash%20me%20if%20you%20can.png)

###Installation:

Clone this repository:
```
git clone https://github.com/daboth/pagan.git
```
and install manually:
```
python setup.py install
```
or install with pip:
```
pip install pagan
```

###Usage example:
```python
# Import the pagan module.
import pagan

# Acquire an arbitrary string.
inpt = 'pagan'

# Use pagan to generate the avatar object based on that input.
# Optional: You can choose which hash function should be used.
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

###Supported Hashes

Hash     | Constant
-------- | --------
md5 | pagan.MD5
sha1 | pagan.SHA1
sha224 | pagan.SHA224
sha256 | pagan.SHA256
sha384 | pagan.SHA384
sha512 | pagan.SHA512


###Testing

To run the pagan tests, you need to install additional python modules. You can choose between pytest and tox. Configure
the tox.ini to test different python versions.

####Using py.test

```
>> pip install pytest
>> pytest
```

####Using tox

```
>> pip install tox
>> tox
```