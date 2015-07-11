from PIL import Image, ImageDraw
import hashgrinder
import paganreader
import random
import hashlib

# Set True to generate debug output in this module.
DEBUG = False

# All images are transparent.
BACKGROUND_COLOR = (0, 0, 0, 0)

FILE_BODY = 'pgn/BODY.pgn'
FILE_BOOTS = 'pgn/BOOTS.pgn'
FILE_SUBFIELD = 'pgn/SUBFIELD.pgn'
FILE_MIN_SUBFIELD = 'pgn/MIN_SUBFIELD.pgn'
FILE_TORSO = 'pgn/TORSO.pgn'
FILE_HAIR = 'pgn/HAIR.pgn'
FILE_SHIELD_DECO = 'pgn/SHIELD_DECO.pgn'

# Out of the box supported
# HASH algorithms from pythons hashlib.
HASH_MD5 = 0
HASH_SHA1 = 1
HASH_SHA224 = 2
HASH_SHA256 = 3
HASH_SHA384 = 4
HASH_SHA512 = 5


def hash_input(inpt, algo=HASH_SHA256):
    """Generates a hash from a given String
    with a specified algorithm and returns the
    hash in hexadecimal form. Default: sha256."""
    if (algo == HASH_MD5):
        hashcode = hashlib.md5()
    elif (algo == HASH_SHA1):
        hashcode = hashlib.sha1()
    elif (algo == HASH_SHA224):
        hashcode = hashlib.sha224()
    elif (algo == HASH_SHA256):
        hashcode = hashlib.sha256()
    elif (algo == HASH_SHA384):
        hashcode = hashlib.sha384()
    elif (algo == HASH_SHA512):
        hashcode = hashlib.sha512()

    hashcode.update(inpt)
    hexhash = hashcode.hexdigest()
    return hexhash


def create_shield_deco_layer(weapons, ip):
    '''Reads the SHIELD_DECO.pgn file and creates
    the shield decal layer.'''
    layer = []
    if weapons[0] in hashgrinder.SHIELDS:
        layer = paganreader.parse_pagan_file(FILE_SHIELD_DECO, ip, invert=False, sym=False)
    return layer


def create_hair_layer(aspect, ip):
    '''Reads the HAIR.pgn file and creates
    the hair layer.'''
    layer = []
    if 'HAIR' in aspect:
        layer = paganreader.parse_pagan_file(FILE_HAIR, ip, invert=False, sym=True)
    return layer


def create_torso_layer(aspect, ip):
    '''Reads the TORSO.pgn file and creates
    the torso layer.'''
    layer = []
    if 'TOP' in aspect:
        layer = paganreader.parse_pagan_file(FILE_TORSO, ip, invert=False, sym=True)
    return layer


def create_subfield_layer(aspect, ip):
    '''Reads the SUBFIELD.pgn file and creates
    the subfield layer.'''
    layer = []
    if 'PANTS' in aspect:
        layer = paganreader.parse_pagan_file(FILE_SUBFIELD, ip, invert=False, sym=True)
    else:
        layer = paganreader.parse_pagan_file(FILE_MIN_SUBFIELD, ip, invert=False, sym=True)

    return layer


def create_boots_layer(aspect, ip):
    '''Reads the BOOTS.pgn file and creates
    the boots layer.'''
    layer = []
    if 'BOOTS' in aspect:
        layer = paganreader.parse_pagan_file(FILE_BOOTS, ip, invert=False, sym=True)
    return layer


def create_weapon_layer(weapons, ip):
    '''Creates the layer for weapons. It is possible to generate two weapons
    based on the weaponstyle decision. The second generated weapon needs
    a different treatment wether a shield is existent or not.'''
    layer_weapon = []

    # Indicates, if a shield was generated.
    is_shield_drawn = False
    for item in weapons:
        # Shields will always be drawn normally.
        if weapons[0] in hashgrinder.SHIELDS:
            layer_weapon += paganreader.parse_pagan_file('pgn/' + item + '.pgn', ip, invert=False, sym=False)
            is_shield_drawn = True
        # Weapons will be drawn normally if they are in the first entry or a shield was drawn.
        elif (weapons.index(item) == 0) or is_shield_drawn:
            layer_weapon += paganreader.parse_pagan_file('pgn/' + item + '.pgn', ip, invert=False, sym=False)
        # When there are two weapons, the second one needs to be drawn on the other hand, so its pixel will be inverted.
        else:
            layer_weapon += paganreader.parse_pagan_file('pgn/' + item + '.pgn', ip, invert=True, sym=False)

    return layer_weapon

# Size variations only allowed on powers of two,
# starting with 16 and ending at 2048. Not used yet.
# Current version only supports a fixed size of 16x16
# virtual pixels.
allowed = [16, 32, 64, 128, 256, 512, 1024, 2048]

# Actual Image size in pixel is fixed in this version of pagan.
imagesize = (128, 128)

# Imagemode ist fixed to RGBA for creating PNG-Files.
imagemode = 'RGBA'

im = Image.new(imagemode, imagesize, BACKGROUND_COLOR)

verticalpixels = []
horizontalpixels = []

# The pixelmap contains the native pixels scaled to virtual pixels
# in the desired resolution. Virtual pixels have a start- and endpoint
# based on the native pixelgrid. Each virtual pixel is
# formatted as followed:
# (startpoint , endpoint , RGBA Color)
pixelmap = []

# Desired virtual resolution of the image output.
# Needs to be lesser or equal to the actual image size.
# (Fixed size for this pagan version.)
resolution = (16, 16)

# Size of a single virtual pixel mapped to the real image size.
dotsize = (imagesize[0] / resolution[0], imagesize[1] / resolution[1])

print ("Virtual pixel size: %s,%s" % (dotsize[0], dotsize[1]))

# Image boundaries. Image starts at (0,0)
max_x = imagesize[0] - 1
max_y = imagesize[1] - 1


def scale_pixels(color, layer):
    """Scales the pixel to the virtual pixelmap."""
    pixelmap = []

    # Scaling the pixel offsets.
    for pix_x in range(max_x + 1):
        for pix_y in range(max_y + 1):

            # Horizontal pixels
            y1 = pix_y * dotsize[0]
            x1 = pix_x * dotsize[1]

            # Vertical pixels
            y2 = pix_y * dotsize[0] + (dotsize[0] - 1)
            x2 = pix_x * dotsize[1] + (dotsize[1] - 1)

            if (y1 <= max_y) and (y2 <= max_y):
                if (x1 <= max_x) and (x2 <= max_x):
                    if (pix_x, pix_y) in layer:
                        pixelmap.append([(y1, x1), (y2, x2), color])
    return pixelmap


def draw_image(pixelmap, img):
    '''Draws the image based on the given pixelmap.'''
    for item in pixelmap:
        color = item[2]

        # Access the rectangle edges.
        pixelbox = (item[0][0], item[0][1], item[1][0], item[1][1])
        draw = ImageDraw.Draw(img)
        draw.rectangle(pixelbox, fill=color)


def setup_pixelmap(ip):
    """Creates and combines all required layers to
    build a pixelmap for creating the virtual
    pixels."""

    # Color distribution.
    # colors = hashgrinder.grindIpForColors(ip)
    colors = hashgrinder.grind_hash_for_colors(ip)
    color_body = colors[0]
    color_subfield = colors[1]
    color_weapon_a = colors[2]
    color_weapon_b = colors[3]
    color_shield_deco = colors[4]
    color_boots = colors[5]
    color_hair = colors[6]
    color_top = colors[7]

    aspect = hashgrinder.grind_hash_for_aspect(ip)


    #Determine weapons and overall aspect of the avatar.
    weapons = hashgrinder.grind_hash_for_weapon(ip)



    if DEBUG:
        print ("Current aspect: %r" % aspect)
        print ("Current weapons: %r" % weapons)

    # There is just one body template. The optional pixels need to be mirrored so
    # the body layout will be symmetric to avoid uncanny looks.
    layer_body = paganreader.parse_pagan_file(FILE_BODY, ip, invert=False, sym=True)

    layer_hair = create_hair_layer(aspect, ip)
    layer_boots = create_boots_layer(aspect, ip)
    layer_torso = create_torso_layer(aspect, ip)
    # TODO: Add second weapon layer to use all colors.
    layer_weapon = create_weapon_layer(weapons, ip)
    layer_subfield = create_subfield_layer(aspect, ip)
    layer_deco = create_shield_deco_layer(weapons, ip)

    pixelmap = scale_pixels(color_body, layer_body)
    pixelmap += scale_pixels(color_top, layer_torso)
    pixelmap += scale_pixels(color_hair, layer_hair)
    pixelmap += scale_pixels(color_subfield, layer_subfield)
    pixelmap += scale_pixels(color_boots, layer_boots)
    pixelmap += scale_pixels(color_weapon_a, layer_weapon)
    pixelmap += scale_pixels(color_shield_deco, layer_deco)

    return pixelmap

def generate_random_ip():
    '''Generates a random ip for
    random avatar generation.'''
    oct1 = random.randint(0, 255)
    oct2 = random.randint(0, 255)
    oct3 = random.randint(0, 255)
    oct4 = random.randint(0, 255)

    return ("%r.%r.%r.%r" % (oct1, oct2, oct3, oct4))


def generate_avatar(str, alg):
    """Generates an PIL image avatar based on the given
    input String. Acts as the main accessor to pagan."""
    img = Image.new(imagemode, imagesize, BACKGROUND_COLOR)
    hashcode = hash_input(str, alg)
    pixelmap = setup_pixelmap(hashcode)
    draw_image(pixelmap, img)
    return img

if __name__ == "__main__":
    # Generate some random avatars and saves them
    # in an output folder when run as main.
    ip = "0.0.0.0"

    for i in range(6):
        blubb = hash_input("Hi", i)
        print ("Hash: %r  Length: %r" % (blubb, len(blubb)))

    input_strings = ["test", "pagan", "python", "github", "avatar", "daboth"]

    for inpt in input_strings:
        img = generate_avatar(inpt, HASH_SHA512)
        filename = ("output/%s.png" % inpt)
        img.save(filename, 'PNG', transparency=0)

    print(int('ffffff', 16))
        #print list(colors)