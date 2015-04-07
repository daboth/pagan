from PIL import Image, ImageDraw
import random

allowed = [16,32,64,128,256,512,1024,2048]

imagesize = (8,8)
imagemode = 'RGBA'

im = Image.new(imagemode, imagesize)

rawpixels = im.load()

print (rawpixels)

verticalpixels = []
horizontalpixels = []

# The pixelmap will scale the native pixels to virtual pixels in the desired resolution.
# Virtual pixels have a start- and endpoint based on the native pixelgrid.
# Each virtual pixel is formatted as followed:
# (startpoint , endpoint , RGBA Color) 
pixelmap = []



resolution = (4,4)

dotsize = (imagesize[0] / resolution[0], imagesize[1] / resolution[1])

print ("Virtual pixel size: %s,%s" % (dotsize[0], dotsize[1]))

print (imagesize[0])

max_x = imagesize[0] - 1
max_y = imagesize[1] - 1 

#Scaling the vertical pixel offsets.
for pix_x in range(max_x + 1):
	for pix_y in range(max_y + 1):
		x = pix_y * dotsize[0]
		y = pix_x * dotsize[1]
		if (y <= max_y):
			if (x <= max_x):
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
	randomcolor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))	
	pixelmap[i].append(randomcolor)



print (verticalpixels)
print (horizontalpixels)
print (pixelmap)
print ("This is PAGAN.")
print (im)