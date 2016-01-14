import math

DEBUG = True

# This screams for an auxiliary module.
OCTET_LENGTH = 4
MAX_DIGIT = 255

# Base of the hexadecimal number system.
HEX_BASE = 16

# TODO: Maybe access the resolution of each
# vertical and horizontal pixel and
# divide them by 2. This apex is fixed for now.
# Used for mirroring the pixels.
IMAGE_APEX = 8

FIXED_PIXEL = 'o'
OPTIONAL_PIXEL = '+'

# TODO: Split into two methods - Finding fixed pixels and optional pixels?
# Less efficient but does not damage my brain. Or generate a tupel of two lists in a seperate method
# and handle them differently.
def parse_pagan_file(filename, hashcode, sym=False, invert=False):
    fd = open(filename, 'r')

    drawmap = []
    optmap = []

    i = 0
    for line in fd:
        j = 0
        for char in line:
            if (char == FIXED_PIXEL):
                drawmap.append((i - 1, j - 1))
            if (char == OPTIONAL_PIXEL):
                optmap.append((i - 1, j - 1))
            j += 1
        i += 1

    fd.close()

    # TODO: Decide for each optional pixel to be displayed
    # in respect of the optmap-size and an the third ip octet.
    # Merge the result with drawmap.
    # print (optmap)
    #print (len(optmap))

    extmap = decideoptionalpixels(optmap, hashcode)

    drawmap += extmap

    if sym:
        drawmap = enforce_vertical_symmetry(drawmap)
    elif invert:
        drawmap = invert_vertical(drawmap)

    return sorted(drawmap)


# Use one of the octets to determine if a pixel is shown or not.
def decideoptionalpixels(optmap, hashcode):
    resmap = []

    # Start with the last character of the hash.
    opt_control = hashcode

    for pixel in optmap:

        control_dec = int(opt_control[-1], HEX_BASE)
        # control_dec = int('7', HEX_BASE)
        opt_control = opt_control[:-1]
        if ((control_dec % 2) == 0):
            resmap.append(pixel)

    return resmap


def enforce_vertical_symmetry(pixmap):
    '''Enforces vertical symmetry of the pixelmap.
    Returns a pixelmap with all pixels mirrored in the middle.
    The initial ones still remain.'''
    mirror = []
    for item in pixmap:
        y = item[0]
        x = item[1]

        if x <= IMAGE_APEX:
            diff_x = diff(x, IMAGE_APEX)
            mirror.append((y, x + (2 * diff_x) - 1))

        if x > IMAGE_APEX:
            diff_x = diff(x, IMAGE_APEX)
            mirror.append((y, x - (2 * diff_x) - 1))

    return mirror + pixmap


def invert_vertical(pixmap):
    '''Inverts all virtual pixels vertically. This results in
    a different pixelmap, where all pixels are mirrored on the
    vertical middle.'''
    mirror = []
    for item in pixmap:
        y = item[0]
        x = item[1]

        if x <= IMAGE_APEX:
            diff_x = diff(x, IMAGE_APEX)
            mirror.append((y, x + (2 * diff_x) - 1))

        if x > IMAGE_APEX:
            diff_x = diff(x, IMAGE_APEX)
            mirror.append((y, x - (2 * diff_x) - 1))

    return mirror


def diff(a, b):
    '''Returns the difference between two values.'''
    return int(math.fabs(a - b))