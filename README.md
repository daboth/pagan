pagan
=====

Welcome to the python avatar generator for absolute nerds.

**Current version: 0.21**

View changes [here](CHANGELOG.md).

Remember those good old days when your own imagination was a big part of the
computer gaming experience? All the limitations of the hardware forced you to
fill the void left by poorly pixelated images by yourself. Well, pagan tries to
give back some of those nostalgic feelings by providing **identicons** in an
oldschool look that are inspired from retro roleplaying adventure games.

Each string input will be hashed and generates a unique avatar image. The purpose
of pagan is to use it for generating a user image in any web application. It is
is meant to replace default user images when creating new accounts or to enhance
comment sections, e.g. visualizing the authors ip address or username.

**The software is currently under development and features the following functions:**

* Process a given string to generate identicons with unique colors and gear.
* The hash function can be chosen from the ones included in pythons hashlib.
* Create the avatar image based on a given resolution.
* Pagan will map all virtual 16x16 Pixels to the real image size.
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

###Usage example:

    # Acquire an arbitrary string.
    inpt = 'pagan'

    # Use pagan to generate the avatar images based on the input.
    # Optional: You can choose, which hash function should be used.
    # Default is HASH_SHA256.
    img = generate_avatar(inpt, HASH_SHA512)

    # Set a filename.
    filename = ("output/%s.png" % inpt)

    # Save the image to file. Look up the Python PIL Documentation
    # for further information about image save functions.
    img.save(filename, 'PNG', transparency=0)


###Supported Hashes

Hash     | Accessor
-------- | --------
md5 | HASH_MD5
sha1 | HASH_SHA1
sha224 | HASH_SHA224
sha256 | HASH_SHA256
sha384 | HASH_SHA384
sha512 | HASH_SHA512
