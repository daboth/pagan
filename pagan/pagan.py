from PIL import Image, ImageDraw
import ipgrinder
import paganreader

DEBUG = True

# ip = "238.111.21.116"

BACKGROUND_COLOR = 0, 0, 0, 0
# ip = "113.227.182.122"
#ip = "194.94.127.7"
#ip = "192.168.2.1"
#ip = "98.12.255.10"
#ip = "128.12.245.21"
#ip = "128.12.245.121"
#ip = "92.226.67.148"
#ip = "127.0.0.1"
#ip = "120.134.212.129"

FILE_BODY = 'pgn/BODY.pgn'
FILE_BOOTS = 'pgn/BOOTS.pgn'
FILE_SUBFIELD = 'pgn/SUBFIELD.pgn'
FILE_MIN_SUBFIELD = 'pgn/MIN_SUBFIELD.pgn'
FILE_TORSO = 'pgn/TORSO.pgn'
FILE_HAIR = 'pgn/HAIR.pgn'
FILE_SHIELD_DECO = 'pgn/SHIELD_DECO.pgn'


def create_shield_deco_layer(weapons, ip):
    layer = []
    if weapons[0] in ipgrinder.SHIELDS:
        layer = paganreader.parsepaganfile(FILE_SHIELD_DECO, ip, invert=False, sym=False)
    return layer


def create_hair_layer(aspect, ip):
    layer = []
    if 'HAIR' in aspect:
        layer = paganreader.parsepaganfile(FILE_HAIR, ip, invert=False, sym=True)
    return layer


def create_torso_layer(aspect, ip):
    layer = []
    if 'TOP' in aspect:
        layer = paganreader.parsepaganfile(FILE_TORSO, ip, invert=False, sym=True)
    return layer


def create_subfield_layer(aspect, ip):
    layer = []
    if 'PANTS' in aspect:
        layer = paganreader.parsepaganfile(FILE_SUBFIELD, ip, invert=False, sym=True)
    else:
        layer = paganreader.parsepaganfile(FILE_MIN_SUBFIELD, ip, invert=False, sym=True)

    return layer


def create_boots_layer(aspect, ip):
    layer = []
    if 'BOOTS' in aspect:
        layer = paganreader.parsepaganfile(FILE_BOOTS, ip, invert=False, sym=True)
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
        if weapons[0] in ipgrinder.SHIELDS:
            layer_weapon += paganreader.parsepaganfile('pgn/' + item + '.pgn', ip, invert=False, sym=False)
            is_shield_drawn = True
        # Weapons will be drawn normally if they are in the first entry or a shield was drawn.
        elif (weapons.index(item) == 0) or is_shield_drawn:
            layer_weapon += paganreader.parsepaganfile('pgn/' + item + '.pgn', ip, invert=False, sym=False)
        # When there are two weapons, the second one needs to be drawn on the other hand, so its pixel will be inverted.
        else:
            layer_weapon += paganreader.parsepaganfile('pgn/' + item + '.pgn', ip, invert=True, sym=False)

    return layer_weapon

# Size variations only allowed on powers of two,
# starting with 16 and ending at 2048.
allowed = [16, 32, 64, 128, 256, 512, 1024, 2048]

imagesize = (256, 256)
imagemode = 'RGBA'

im = Image.new(imagemode, imagesize, BACKGROUND_COLOR)

rawpixels = im.load()

print (rawpixels)

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
# (fixed size for pagan)
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


def draw_image(pixelmap):
    for item in pixelmap:
        color = item[2]
        #Access the rectangle edges.
        pixelbox = (item[0][0], item[0][1], item[1][0], item[1][1])
        draw = ImageDraw.Draw(im)
        draw.rectangle(pixelbox, fill=color)


def setup_pixelmap(ip):
    '''Creates and combines all required layers to
    build a pixelmap for creating the virtual
    pixels.'''

    # Color distribution.
    colors = ipgrinder.grindIpForColors(ip)
    color_body = colors[0]
    color_aspect = colors[1]
    color_weapon = colors[2]
    color_aspect_details = colors[3]
    color_shield_deco = colors[4]

    #Determine weapons and overall aspect of the avatar.
    weapons = ipgrinder.grindIpForWeapon(ip)
    aspect = ipgrinder.grind_for_aspect(ip)

    if DEBUG:
        print ("Current aspect: %r" % aspect)
        print ("Current weapons: %r" % weapons)

    # There is just one body template. The optional pixels need to be mirrored so
    # the body layout will be symmetric to avoid uncanny looks.
    layer_body = paganreader.parsepaganfile(FILE_BODY, ip, invert=False, sym=True)

    layer_hair = create_hair_layer(aspect, ip)
    layer_boots = create_boots_layer(aspect, ip)
    layer_torso = create_torso_layer(aspect, ip)
    layer_weapon = create_weapon_layer(weapons, ip)
    layer_subfield = create_subfield_layer(aspect, ip)
    layer_deco = create_shield_deco_layer(weapons, ip)

    pixelmap = scale_pixels(color_body, layer_body)
    pixelmap += scale_pixels(color_aspect_details, layer_torso)
    pixelmap += scale_pixels(color_aspect_details, layer_hair)
    pixelmap += scale_pixels(color_aspect, layer_subfield)
    pixelmap += scale_pixels(color_aspect_details, layer_boots)
    pixelmap += scale_pixels(color_weapon, layer_weapon)
    pixelmap += scale_pixels(color_shield_deco, layer_deco)

    return pixelmap


if __name__ == "__main__":
    #ip = "162.233.4.12"
    ip = "238.111.21.116"
    #ip = "188.88.88.222"
    #ip = "215.128.122.12"
    #ip = "125.38.2.22"
    #ip = "110.11.121.221"
    #ip = "135.238.22.33"
    pixelmap = setup_pixelmap(ip)
    #pixelmap = create_layers("192.168.2.1")

    #print ("PIXELMAP: %r" % pixelmap)
    draw_image(pixelmap)
    #pixelmap = scale_pixels(color_weapon, layer_weapon)
    #draw_layer(pixelmap)
    #weapons = scale_pixels(layer_weapon)
    #draw_layer(pixelmap)
    im.show()

    #print ("Length: %r" % len(pixelmap))
