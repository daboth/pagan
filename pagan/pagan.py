from PIL import Image, ImageDraw
import random
import ipgrinder
import paganreader

# ip = "238.111.21.116"


ip = "113.227.182.122"
colors = ipgrinder.grindIpForColors(ip)
filename = 'example_weapon_short.pgn'
# filename = 'test.pgn'
drawmap = paganreader.parsepaganfile(filename, ip)
print ("Drawmap: %r" % drawmap)

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

print (imagesize[0])

# Image boundaries. Image starts at (0,0)
max_x = imagesize[0] - 1
max_y = imagesize[1] - 1

# # Scaling the vertical pixel offsets.
# for pix_x in range(max_x + 1):
#     for pix_y in range(max_y + 1):
#         x = pix_y * dotsize[0]
#         y = pix_x * dotsize[1]
#         if y <= max_y:
#             if x <= max_x:
#                 # TODO: Maybe add specific color here, when
#                 # all layers of body/armor/weapon are applied.
#                 if (pix_x, pix_y) in drawmap:
#                     verticalpixels.append([(x, y), (200,200,200)])
#                 else:
#                     verticalpixels.append([(x, y), (0,0,0)])
#
# #Scaling the horizontal pixel offsets.
# for pix_x in range(max_x + 1):
#     for pix_y in range(max_y + 1):
#         x = pix_y * dotsize[0] + (dotsize[0] - 1)
#         y = pix_x * dotsize[1] + (dotsize[1] - 1)
#         if y <= max_y:
#             if x <= max_x:
#                 if (pix_x, pix_y) in drawmap:
#                     horizontalpixels.append(((x, y), (200,200,200)))
#                 else:
#                     horizontalpixels.append(((x, y), (0,0,0)))


def scale_pixels():
    """Scales the pixel to the virtual pixelmap"""
    pixelmap = []

    #Scaling the pixel offsets.
    for pix_x in range(max_x + 1):
        for pix_y in range(max_y + 1):

            # Horicontal pixels
            x1 = pix_y * dotsize[0]
            y1 = pix_x * dotsize[1]

            # Vertical pixels
            x2 = pix_y * dotsize[0] + (dotsize[0] - 1)
            y2 = pix_x * dotsize[1] + (dotsize[1] - 1)

            if (y1 <= max_y) and (y2 <= max_y):
                if (x1 <= max_x) and (x2 <= max_x):
                    if (pix_x, pix_y) in drawmap:
                        pixelmap.append([(x1,y1), (x2,y2), (200, 200, 200)])
                    else:
                        pixelmap.append([(x1,y1), (x2,y2), (0, 0, 0)])

    return pixelmap

pixelmap = scale_pixels()

# #Generating the pixelmap
# for i in range(len(verticalpixels)):
#     pixelmap.append([verticalpixels[i], horizontalpixels[i]])

#Add random colors to the pixelmap (testing purpose)
# for i in range(len(pixelmap)):
#     randomcolor = colors[random.randint(0, len(colors) - 1)]
#     pixelmap[i].append(randomcolor)

for item in pixelmap:
    color = item[2]
    #Access the rectangle edges.
    pixelbox = (item[0][0], item[0][1], item[1][0], item[1][1])
    draw = ImageDraw.Draw(im)
    draw.rectangle(pixelbox, fill=color)

if __name__ == "__main__" :
    scale_pixels()
    im.show()
    print (verticalpixels)
    print (horizontalpixels)
    print (pixelmap)
    print ("This is PAGAN.")
    print (im)