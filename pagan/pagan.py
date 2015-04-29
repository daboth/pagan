from PIL import Image, ImageDraw
import random
import ipgrinder
import paganreader

ip = "238.111.21.116"

BACKGROUND_COLOR = 0, 0, 0, 0
#ip = "113.227.182.122"
#ip = "194.94.127.7"
# ip = "192.168.2.1"
#ip = "98.12.255.10"
#ip = "128.12.245.21"
#ip = "128.12.245.121"
ip = "92.226.67.148"
colors = ipgrinder.grindIpForColors(ip)
weapons = ipgrinder.grindIpForWeapon(ip)

#weapons = ['GREATAXE']



# Color distribution.
color_body = colors[0]
color_aspect = colors[1]
color_weapon = colors[2]
color_aspect_details = colors[3]

FILE_BODY = 'pgn/BODY.pgn'

#layers = create_layers(ip)


def create_layers(ip):
    '''Creates all layers to generate the image based off
    the respective .pgn file decided by the pagan parser.'''

    # Used to draw the basic body of the figure.
    layer_body = paganreader.parsepaganfile(FILE_BODY, ip, invert=False, sym=True)
    # Used to draw the boots and the torso armor if existent.
    layer_aspect_boots_torso = 0
    # Used to draw weapons and shields.
    layer_weapons = create_weapon_layer(weapons)
    # Used to draw decoration on shields and hair if existent and the subfield armor.
    layer_aspect_deco_subfield_hair = 0

    # Apply all layers. Every layer is added to the drawmap and each virtual pixel
    # will be gradually drawn. The last applied layers virtual pixel will then
    # override each previously drawn pixel.
    layers = layer_body + \
             layer_aspect_boots_torso +\
             layer_weapons +\
             layer_aspect_deco_subfield_hair

    return layers

# There is just one body template. The optional pixels need to be mirrored so
# the body layout will be symmetric to avoid uncanny looks.
layer_body = paganreader.parsepaganfile(FILE_BODY, ip, invert=False, sym=True)

layer_weapon = []

hasShield = False
for item in weapons:
    # The first weapon will always be drawn normally.
    if (item == 'SHIELD') or (weapons.index(item) == 0):
        layer_weapon += paganreader.parsepaganfile('pgn/' + item + '.pgn', ip, invert=False, sym=False)
        hasShield = True
    # If a shield was drawn, the weapon will be drawn normally.
    elif hasShield:
        layer_weapon += paganreader.parsepaganfile('pgn/' + item + '.pgn', ip, invert=False, sym=False)
    # When there are two weapons, the second one needs to be drawn on the other hand, so its pixel will be inverted.
    else:
        layer_weapon += paganreader.parsepaganfile('pgn/' + item + '.pgn', ip, invert=True, sym=False)


def create_weapon_layer(weapons):
    '''Creates the layer for weapons. It is possible to generate two weapons
    based on the weaponstyle decision. The second generated weapon needs
    a different treatment wether a shield is existent or not.'''
    layer_weapon = []

    # Indicates, if a shield was generated.
    hasShield = False
    for item in weapons:
        # The first weapon will always be drawn normally.
        if (item == 'SHIELD') or (weapons.index(item) == 0):
            layer_weapon += paganreader.parsepaganfile('pgn/' + item + '.pgn', ip, invert=False, sym=False)
            hasShield = True
        # If a shield was drawn, the weapon will be drawn normally.
        elif hasShield:
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
    """Scales the pixel to the virtual pixelmap"""
    pixelmap = []

    #Scaling the pixel offsets.
    for pix_x in range(max_x + 1):
        for pix_y in range(max_y + 1):

            # Horicontal pixels
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


def superimpose_layer(pixelmap, layer):
    return pixelmap + layer


if __name__ == "__main__":
    pixelmap = scale_pixels(color_body, layer_body)
    pixelmap += scale_pixels(color_weapon, layer_weapon)
    draw_image(pixelmap)
    #pixelmap = scale_pixels(color_weapon, layer_weapon)
    #draw_layer(pixelmap)
    #weapons = scale_pixels(layer_weapon)
    #draw_layer(pixelmap)
    im.show()

    print ("Length: %r" % len(pixelmap))
    print (weapons)
