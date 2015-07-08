import math

# Number of colors.
COLOR_QUANTITY = 8

# Length of a color in hex.
HEX_COLOR_LEN = 6

# Base of the hexadecimal number system.
HEX_BASE = 16

# To generate 8 unique colors, hashes need to
# contain at least this many characters.
MINIMUM_HASH_LEN = COLOR_QUANTITY * HEX_COLOR_LEN

# The first 8 Bits of a hash
# determine the avatars overall aspect.
ASPECT_CONTROL_BITS = 8

max_digitsum = 255.0 * 4
max_digit = 255.0

# Set True to generate debug output in this module.
DEBUG = True

WEAPONSTYLES = ['ONEHANDED_ONEHANDED',
                'SHIELD_ONEHANDED',
                'ONEHANDED',
                'TWOHANDED']

TWOHANDED_WEAPONS = ['GREATSWORD',
                     'BIGHAMMER',
                     'GREATMACE',
                     'GREATAXE',
                     'WAND']

ONEHANDED_WEAPONS = ['SWORD',
                     'HAMMER',
                     'AXE',
                     'FLAIL',
                     'MACE',
                     'DAGGER']

SHIELDS = ['LONGSHIELD',
           'ROUNDSHIELD',
           'BUCKLER',
           'SHIELD']

# The different aspects an avatar can take.
ASPECTSTYLES = [['HAIR'],
                ['HAIR', 'PANTS', 'TOP'],
                ['HAIR', 'PANTS'],
                ['HAIR', 'BOOTS', 'TOP'],
                ['HAIR', 'BOOTS'],
                ['HAIR', 'TOP'],
                ['HAIR', 'PANTS', 'BOOTS'],
                ['HAIR', 'PANTS', 'BOOTS', 'TOP'],
                ['PANTS', 'BOOTS', 'TOP'],
                ['PANTS', 'BOOTS'],
                ['PANTS', 'TOP'],
                ['PANTS'],
                ['BOOTS', 'TOP'],
                ['BOOTS'],
                ['TOP'],
                []]


def init_weapon_list():
    """Initialize the possible weapon
    combinations."""
    twohand = []
    for item in TWOHANDED_WEAPONS:
        twohand.append([item])

    onehand = []
    for item in ONEHANDED_WEAPONS:
        onehand.append([item])

    shield = SHIELDS

    dualwield_variations = []
    weapon_shield_variations = []

    for item in ONEHANDED_WEAPONS:
        for i in ONEHANDED_WEAPONS:
            dualwield_variations.append([item, i])
        for j in shield:
            weapon_shield_variations.append([j, item])

    return twohand + onehand + dualwield_variations + weapon_shield_variations


def grind_hash_for_colors(hashcode):
    """Extracts information from the hashcode
    to generate different colors. Returns a
    list of colors in (r,g,b) tupels."""

    # When using smaller hash algorithms like MD5 or SHA1,
    # the number of bits does not provide enough information
    # to generate unique colors. Instead the hash is internally
    # appended by itself to fit the MINIMUM_HASH_LEN.
    # This leads to smaller hashes displaying less color
    # variatons, depicting the insecurity of the used hashes.
    while (len(hashcode) < MINIMUM_HASH_LEN):
        chardiff = diff(len(hashcode), MINIMUM_HASH_LEN)
        if DEBUG:
            print ("Hashcode: %r with length: %d is too small. Appending difference." % (hashcode, len(hashcode)))
        hashcode += hashcode[:chardiff]
        if DEBUG:
            print ("Hash is now: %r with length: %d" % (hashcode, len(hashcode)))

    hashparts = split_sequence(hashcode, HEX_COLOR_LEN)

    colors = []

    for i in range(COLOR_QUANTITY):
        colors.append(hex2rgb(hashparts[i]))
    if DEBUG:
        print ("Generated colors: %r" % colors)
    return colors


# def split_sequence(seq, n):
# """Generates subsequences from a
#     sequence splitted at every position n."""
#     while seq:
#         yield seq[:n]
#         seq = seq[n:]
#

def split_sequence(seq, n):
    """Generates tokens of length n from a sequence.
    The last token may be of smaller length."""
    tokens = []
    while seq:
        tokens.append(seq[:n])
        seq = seq[n:]
    return tokens


# Grinds the ip address for an aspect style to draw on the pixelmap.
def grind_for_aspect(ip):
    digitsum = getDigitSum(ip)
    decision = mapDecision(max_digitsum, len(ASPECTSTYLES), digitsum)
    print decision
    return chooseAspectStyle(decision)


# Grinds the ip address for a weapon to draw on the pixelmap.
# Utilizes the last ip octet for maximum difference. This helps
# to get more different results due to the last octet being the most
# variant in local areas.
def grindIpForWeapon(ip):
    weaponlist = init_weapon_list()
    print len(weaponlist)
    lastdigit = getLastOctet(ip)
    decision = mapDecision(max_digit, len(weaponlist), lastdigit)
    print decision

    weapon = []
    choice = []

    for i in range(len(weaponlist)):
        if (i < decision):
            choice = weaponlist[i]

    for item in choice:
        weapon.append(item)

    return weapon


# Chooses a specific weapon from predefined weaponstyle.
def chooseWeapon(weapons, digit):
    decision = mapDecision(max_digit, len(weapons), digit)
    choice = []
    for i in range(len(weapons)):
        if (i < decision):
            choice = weapons[i]
    return choice


def chooseWeaponstyle(decision):
    choice = []
    for i in range(len(WEAPONSTYLES)):
        if (i < decision):
            choice = WEAPONSTYLES[i]
    return choice


def chooseAspectStyle(decision):
    choice = []
    for i in range(len(ASPECTSTYLES)):
        if (i < decision):
            choice = ASPECTSTYLES[i]
    return choice


# Maps the domain to a number of decisions.
def mapDecision(max_digitsum, num_decisions, digitsum):
    return (num_decisions / (max_digitsum + 1)) * (digitsum + 1)


# Returns the digit sum of all ip octets.
def getDigitSum(ip):
    octets = ip.split('.')
    digitsum = 0

    for item in octets:
        digitsum += int(item)

    return digitsum


def hex2rgb(hexvalue):
    """Converts a given hex color to
    its respective rgb color."""

    # Make sure the possible '#' char is eliminated
    # before processing the color.
    if ('#' in hexvalue):
        hexcolor = hexvalue.replace('#', '')
    else:
        hexcolor = hexvalue

    # Hex colors have a fixed length of 6 characters excluding the '#'
    if (len(hexcolor) != 6):
        print ("Unexpected length of hex color value.\nSix characters excluding \'#\' expected.")
        return 0

    # Convert each part of the hex to
    # an RGB color value.
    r = int(hexcolor[0:2], HEX_BASE)
    g = int(hexcolor[2:4], HEX_BASE)
    b = int(hexcolor[4:6], HEX_BASE)

    return r, g, b


#Returns the last octet of the ip address.
def getLastOctet(ip):
    octets = ip.split('.')
    return int(octets[len(octets) - 1])


def diff(a, b):
    '''Returns the difference between two values.'''
    return int(math.fabs(a - b))


if __name__ == "__main__":
    hash1 = "0396233d5b28eded8e34c1bf9dc80fae34756743594b9e5ae67f4f7d124d2e3d"
    hash2 = "ef101b0bc42f41e23e325f3da71daeff43ff7df9d41ff268e53a06c767de8487"
    hash3 = "ca4da36c48be1c0b87a7d575c73f6e42"

    h1 = grind_hash_for_colors(hash1)
    h2 = grind_hash_for_colors(hash2)
    h3 = grind_hash_for_colors(hash3)

    print h1



    #print hashlib.algorithms

    seq = split_sequence(hash1, 6)
    print seq

    hex2rgb('#ffffff')
    hex2rgb('#ffff00')
    hex2rgb('#f5f5f5')

