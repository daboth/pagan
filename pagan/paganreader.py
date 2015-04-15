fixed_pixel = 'o'

def parsePaganFile(filename):
	fd = open(filename, 'r')
	#fd.next()
	drawmap = []

	i = 1
	for line in fd:
		j = 1
		for char in line:
			#parsePaganFileif (char == ' ') or (char == '#') or (char == '\n'):
				#print ("%r: Line %s, Row %s " % (char, i,j))
			if (char == fixed_pixel):
				#print ("\nPixel found! Line %s, Row %s \n" % (i,j))
				drawmap.append((i - 1, j - 1))
			j += 1
		i += 1

	fd.close()

	return drawmap


filename = 'example_weapon_short.pgn'
dmap = parsePaganFile(filename)

print (dmap)