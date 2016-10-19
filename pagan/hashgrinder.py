import math

# Number of colors.
COLOR_QUANTITY = 8

# Length of a color in hex.
HEX_COLOR_LEN = 6

# Base of the hexadecimal number system.
HEX_BASE = 16

# To generate unique colors, hashes need to
# contain at least this many characters.
MINIMUM_HASH_LEN = COLOR_QUANTITY * HEX_COLOR_LEN

# The first and second six characters of a hash
# determine the avatars overall aspect.
ASPECT_CONTROL_LEN = 6

# Decimal representation of hexadecimal 'ffffff'
# as the maximum value for aspect decisions.
MAX_DECISION_VALUE = 16777215

# Set True to generate debug output in this module.
DEBUG = False

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
    # variatons, depicting the insecurity of small hashes.
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


def split_sequence(seq, n):
    """Generates tokens of length n from a sequence.
    The last token may be of smaller length."""
    tokens = []
    while seq:
        tokens.append(seq[:n])
        seq = seq[n:]
    return tokens


# Grinds the ip address for an aspect style to draw on the pixelmap.
def grind_hash_for_aspect(hashcode):
    # aspect_control = split_sequence(hashcode, ASPECT_CONTROL_CHARS)
    aspect_control = hashcode[:ASPECT_CONTROL_LEN]
    #print aspect_control
    hash_dec_value = int(aspect_control, HEX_BASE)
    decision = map_decision(MAX_DECISION_VALUE, len(ASPECTSTYLES), hash_dec_value)
    if DEBUG:
        print ("Aspect decision: %r" %decision)
    return choose_aspect(decision)


def grind_hash_for_weapon(hashcode):
    """ Grinds the given hashcode for a weapon to draw on
    the pixelmap. Utilizes the second six characters from the
    hashcode."""

    weaponlist = init_weapon_list()
    # The second six characters of the hash
    # control the weapon decision.
    weapon_control = hashcode[ASPECT_CONTROL_LEN:(ASPECT_CONTROL_LEN * 2)]

    # Decimal value of the hash chunk to map.
    hash_dec_value = int(weapon_control, HEX_BASE)
    decision = map_decision(MAX_DECISION_VALUE, len(weaponlist), hash_dec_value)

    return choose_weapon(decision, weaponlist)


def choose_weapon(decision, weapons):
    """Chooses a weapon from a given list
    based on the decision."""
    choice = []
    for i in range(len(weapons)):
        if (i < decision):
            choice = weapons[i]
    return choice


def choose_aspect(decision):
    """Chooses a style from ASPECTSTYLES
    based on the decision."""
    choice = []
    for i in range(len(ASPECTSTYLES)):
        if (i < decision):
            choice = ASPECTSTYLES[i]
    return choice


def map_decision(max_digitsum, num_decisions, digitsum):
    """Maps the domain to a number of decisions."""
    return (num_decisions / (float(max_digitsum) + 1)) * (float(digitsum) + 1)


def hex2rgb(hexvalue):
    """Converts a given hex color to
    its respective rgb color."""

    # Make sure a possible '#' char is eliminated
    # before processing the color.
    if ('#' in hexvalue):
        hexcolor = hexvalue.replace('#', '')
    else:
        hexcolor = hexvalue

    # Hex colors have a fixed length of 6 characters excluding the '#'
    # TODO: Include custom exception here, even if it should never happen.
    if (len(hexcolor) != 6):
        print ("Unexpected length of hex color value.\nSix characters excluding \'#\' expected.")
        return 0

    # Convert each two characters of
    # the hex to an RGB color value.
    r = int(hexcolor[0:2], HEX_BASE)
    g = int(hexcolor[2:4], HEX_BASE)
    b = int(hexcolor[4:6], HEX_BASE)

    return r, g, b


def diff(a, b):
    """Returns the difference between two values."""
    return int(math.fabs(a - b))


if __name__ == "__main__":

    # Testing some hashes.
    hash1 = "0396233d5b28eded8e34c1bf9dc80fae34756743594b9e5ae67f4f7d124d2e3d"
    hash2 = "ef101b0bc42f41e23e325f3da71daeff43ff7df9d41ff268e53a06c767de8487"
    hash3 = "ca4da36c48be1c0b87a7d575c73f6e42"

    h1 = grind_hash_for_colors(hash1)
    h2 = grind_hash_for_colors(hash2)
    h3 = grind_hash_for_colors(hash3)

    hex2rgb('#ffffff')
    hex2rgb('#ffff00')
    hex2rgb('#f5f5f5')