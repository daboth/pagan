from PIL import Image, ImageDraw
import random
import ipgrinder
import paganreader

# ip = "238.111.21.116"

BACKGROUND_COLOR = 0,0,0,0
ip = "113.227.182.122"
#ip = "192.168.2.1"
#ip = "98.12.255.10"
colors = ipgrinder.grindIpForColors(ip)

# Color distribution.
color_body = colors[0]
color_attire = colors[1]
color_weapon = colors[2]
color_details = colors[3]

filename = 'example_weapon_short.pgn'
# filename = 'test.pgn'
file_body = 'pgn/body.pgn'
file_weapon = 'pgn/wand.pgn'

layer_body = paganreader.parsepaganfile(file_body, ip, invert=False, sym=True)
layer_weapon = paganreader.parsepaganfile(file_weapon, ip, invert=False, sym=False)
#print ("Drawmap: %r" % drawmap)

# Size variations only allowed on powers of two,
# starting with 16 and ending at 2048.
allowed = [16, 32, 64, 128, 256, 512, 1024, 2048]

imagesize = (256, 256)
imagemode = 'RGBA'

im = Image.new(imagemode, imagesize)

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
                        pixelmap.append([(y1,x1), (y2,x2), color])
                    else:
                        pixelmap.append([(y1,x1), (y2,x2), BACKGROUND_COLOR])

    return pixelmap



# #Generating the pixelmap
# for i in range(len(verticalpixels)):
#     pixelmap.append([verticalpixels[i], horizontalpixels[i]])

#Add random colors to the pixelmap (testing purpose)
# for i in range(len(pixelmap)):
#     randomcolor = colors[random.randint(0, len(colors) - 1)]
#     pixelmap[i].append(randomcolor)

def draw_image(pixelmap):
    for item in pixelmap:
        color = item[2]
        #Access the rectangle edges.
        pixelbox = (item[0][0], item[0][1], item[1][0], item[1][1])
        draw = ImageDraw.Draw(im)
        draw.rectangle(pixelbox, fill=color)

def superimpose_layer(pixelmap, layer):
    for item in pixelmap:
        print "Bla"

if __name__ == "__main__" :
    pixelmap = scale_pixels(color_body, layer_body)
    #pixelmap + scale_pixels(color_weapon, layer_weapon)
    draw_image(pixelmap)
    #pixelmap = scale_pixels(color_weapon, layer_weapon)
    #draw_layer(pixelmap)
    #weapons = scale_pixels(layer_weapon)
    #draw_layer(pixelmap)
    im.show()

    print ("Length: %r" % len(pixelmap))
