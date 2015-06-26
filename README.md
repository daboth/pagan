pagan
=====

Welcome to the python avatar generator for absolute nerds.

**Current version: 0.11**

Remember those good old days when your own imagination was a big part of your
computer gaming experience? All the limitations of the hardware forced you to
fill the void left by poorly pixelated images by yourself. Well, pagan tries to
give back some of those nostalgic feelings by providing identicons in an
oldschool look that are inspired from retro roleplaying adventure games.

Each ipv4 address will generate a unique Avatar image you are free to use. The purpose
of pagan is to use it as a user image in any web application. It is based on the
IPv4 address that logged in when creating an account or posted something.

The software is currently under development and is going to feature the following functions:

* Process a given ip4 adress to generate identicons with unique colors and gear
* Generate random avatar images
* Create the avatar image based on a given resolution
* Pagan will map all virtual 16x16 Pixels to the real image size.
* Expand pagan by adding new weapons or gear.
* Enjoy the nostalgia!

###Usage example:

    # Aquire an IPv4 address in String form.
    ip = "192.168.2.1"
    # Use pagan to generate the avatar image based on the IP.
    img = generate_avatar(ip)
    # Choose a filename
    filename = ("%s.png" % ip)
    # Save the image to file. Look up the Python PIL Documentation
    # for further information about image save functions.
    img.save(filename, 'PNG', transparency=0)


###Example avatars:

* 13.40.146.216 ![13.40.146.216](/images/13.40.146.216.png)
* 68.124.253.57 ![68.124.253.57](/images/68.124.253.57.png)
* 108.214.78.29 ![108.214.78.29](/images/108.214.78.29.png)
* 123.239.247.36 ![123.239.247.36](/images/123.239.247.36.png)
* 218.252.22.97 ![218.252.22.97](/images/218.252.22.97.png)
* 227.96.80.11 ![227.96.80.11](/images/227.96.80.11.png)
* 234.162.46.165 ![234.162.46.165](/images/234.162.46.165.png)
* 245.45.55.139 ![245.45.55.139](/images/245.45.55.139.png)
* 252.170.70.52 ![252.170.70.52](/images/252.170.70.52.png)
* 254.5.11.117 ![254.5.11.117](/images/254.5.11.117.png)

