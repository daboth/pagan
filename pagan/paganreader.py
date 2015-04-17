fixed_pixel = 'o'
optional_pixel = '+'

def parsePaganFile(filename):
	fd = open(filename, 'r')
	#fd.next()
	drawmap = []
	optmap = []

	i = 1
	for line in fd:
		j = 1
		for char in line:
			#parsePaganFileif (char == ' ') or (char == '#') or (char == '\n'):
				#print ("%r: Line %s, Row %s " % (char, i,j))
			if (char == fixed_pixel):
				#print ("\nPixel found! Line %s, Row %s \n" % (i,j))
				drawmap.append((i - 1, j - 1))
			if (char == optional_pixel):
				optmap.append((i - 1, j - 1))
			j += 1
		i += 1

	fd.close()

	# TODO: Decide for each optional pixel to be displayed
	# in respect of the optmap-size and an the third ip octet.
	# Merge the result with drawmap.
	print (optmap)
	print (len(optmap))

	extmap = readOptionalPixel(optmap)
	print (extmap)

	return drawmap + extmap

def readOptionalPixel(optmap, ip):
	return [(0, 2)]


filename = 'example_weapon_short.pgn'
dmap = parsePaganFile(filename)

print (dmap)
