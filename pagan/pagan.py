from PIL import Image, ImageDraw
import random
import ipgrinder

ip = "238.111.21.116"
colors = ipgrinder.grindIpForColors(ip)

# Size variations only allowed on powers of two,
# starting with 16 and ending at 2048.
allowed = [16,32,64,128,256,512,1024,2048]

imagesize = (96,96)
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
resolution = (16,16)

# Size of a single virtual pixel mapped to the real image size.
dotsize = (imagesize[0] / resolution[0], imagesize[1] / resolution[1])

print ("Virtual pixel size: %s,%s" % (dotsize[0], dotsize[1]))

print (imagesize[0])

# Image boundaries. Image starts at (0,0)
max_x = imagesize[0] - 1
max_y = imagesize[1] - 1

#Scaling the vertical pixel offsets.
for pix_x in range(max_x + 1):
	for pix_y in range(max_y + 1):
		x = pix_y * dotsize[0]
		y = pix_x * dotsize[1]
		if (y <= max_y):
			if (x <= max_x):
				#TODO: Maybe add specific color here, when
				#all layers of body/armor/weapon are applied.
				verticalpixels.append((x, y))

#Scaling the horizontal pixel offsets.
for pix_x in range(max_x + 1):
	for pix_y in range(max_y + 1):
		x = pix_y * dotsize[0] + (dotsize[0] - 1)
		y = pix_x * dotsize[1] + (dotsize[1] - 1)
		if (y <= max_y):
			if (x <= max_x):
				horizontalpixels.append((x, y))

#Generating the pixelmap
for i in range(len(verticalpixels)):
	pixelmap.append([verticalpixels[i], horizontalpixels[i]])

#Add random colors to the pixelmap (testing purpose)
for i in range(len(pixelmap)):
	randomcolor = colors[random.randint(0,len(colors) - 1)]
	pixelmap[i].append(randomcolor)

for item in pixelmap:
	color = item[2]
	#Access the rectangle edges.
	pixelbox = (item[0][0], item[0][1], item[1][0],item[1][1])
	draw = ImageDraw.Draw(im)
	draw.rectangle(pixelbox, fill=color)

im.show()
print (verticalpixels)
print (horizontalpixels)
print (pixelmap)
print ("This is PAGAN.")
print (im)