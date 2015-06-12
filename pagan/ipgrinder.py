max_digitsum = 255.0 * 4
max_digit = 255.0

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

# Split into two aspectstyles because of the color mixing in the layers.
# Paganreader tries to read a file with this name, resulting in reading all
# the pixels into one layer, but the intention was to generate only two aspects
# in the same color.
ASPECTSTYLES = [['HAIR'],
                ['HAIR', 'PANTS', 'BOOTS'],
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

def grindIpForColors(ip):
    octets = ip.split('.')
    rgb1 = (int(octets[0]), int(octets[1]), int(octets[2]))
    rgb2 = (int(octets[1]), int(octets[2]), int(octets[3]))
    rgb3 = (int(octets[2]), int(octets[3]), int(octets[0]))
    rgb4 = (int(octets[3]), int(octets[0]), int(octets[1]))
    rgb5 = (int(octets[2]), int(octets[1]), int(octets[3]))

    return [rgb1, rgb2, rgb3, rgb4, rgb5]

# Grinds the ip address for an aspect style to draw on the pixelmap.
def grind_for_aspect(ip):
    digitsum = getDigitSum(ip)
    decision = mapDecision(max_digitsum, len(ASPECTSTYLES), digitsum)
    return chooseAspectStyle(decision)


# Grinds the ip address for a weapon to draw on the pixelmap.
# Utilizes the last ip octet for maximum difference. This helps
# to get more different results due to the last octet being the most
# variant in local areas. 
def grindIpForWeapon(ip):
    digitsum = getDigitSum(ip)
    lastdigit = getLastOctet(ip)
    decision = mapDecision(max_digitsum, len(WEAPONSTYLES), digitsum)
    WEAPONSTYLE = chooseWeaponstyle(decision)

    weapon = []

    if (WEAPONSTYLE == 'TWOHANDED'):
        weapon.append(chooseWeapon(TWOHANDED_WEAPONS, lastdigit))

    if (WEAPONSTYLE == 'ONEHANDED'):
        weapon.append(chooseWeapon(ONEHANDED_WEAPONS, lastdigit))

    if (WEAPONSTYLE == 'SHIELD_ONEHANDED'):
        weapon.append(chooseWeapon(SHIELDS, lastdigit))
        weapon.append(chooseWeapon(ONEHANDED_WEAPONS, lastdigit))

    if (WEAPONSTYLE == 'ONEHANDED_ONEHANDED'):
        weapon.append(chooseWeapon(ONEHANDED_WEAPONS, lastdigit))
        weapon.append(chooseWeapon(ONEHANDED_WEAPONS, max_digit - lastdigit))

    return weapon



# Chooses a specific weapon from predefined weaponstyle.
def chooseWeapon(weapons, digit):
    decision = mapDecision(max_digit, len(weapons), digit)
    choice = ''
    for i in range(len(weapons)):
        if (i < decision):
            choice = weapons[i]
    return choice


def chooseWeaponstyle(decision):
    for i in range(len(WEAPONSTYLES)):
        if (i < decision):
            choice = WEAPONSTYLES[i]
    return choice

def chooseAspectStyle(decision):
    for i in range(len(ASPECTSTYLES)):
        if (i < decision):
            choice = ASPECTSTYLES[i]
    return choice


# Maps the domain to a number of descisions.
def mapDecision(max_digitsum, num_decisions, digitsum):
    return (num_decisions / max_digitsum) * digitsum


#Returns the digit sum of all ip octets.
def getDigitSum(ip):
    octets = ip.split('.')
    digitsum = 0

    for item in octets:
        digitsum += int(item)

    return digitsum


#Returns the last octet of the ip address.
def getLastOctet(ip):
    octets = ip.split('.')
    return int(octets[len(octets) - 1])


if __name__ == "__main__" :

    ###############################TESTS#################################
    ip = "238.111.21.116"
    ip2 = "1.24.21.16"
    ip3 = "238.211.271.166"
    ip4 = "192.238.12.231"
    ip5 = "12.128.12.21"
    ip6 = "12.168.2.1"
    ip7 = "133.100.13.11"
    ip8 = "127.0.0.1"
    ip9 = "127.34.45.54"
    ip10 = "12.11.1.214"

    print ("####### WEAPONS #######")
    print ("IP1: %s\tChoice: %s" % (ip, grindIpForWeapon(ip)))
    print ("IP2: %s\tChoice: %s" % (ip2, grindIpForWeapon(ip2)))
    print ("IP3: %s\tChoice: %s" % (ip3, grindIpForWeapon(ip3)))
    print ("IP4: %s\tChoice: %s" % (ip4, grindIpForWeapon(ip4)))
    print ("IP5: %s\tChoice: %s" % (ip5, grindIpForWeapon(ip5)))
    print ("IP6: %s\tChoice: %s" % (ip6, grindIpForWeapon(ip6)))
    print ("IP7: %s\tChoice: %s" % (ip7, grindIpForWeapon(ip7)))
    print ("IP8: %s\tChoice: %s" % (ip8, grindIpForWeapon(ip8)))
    print ("IP9: %s\tChoice: %s" % (ip9, grindIpForWeapon(ip9)))
    print ("IP10: %s\tChoice: %s" % (ip10, grindIpForWeapon(ip10)))
    print ("\n####### ASPECTS #######")
    print ("IP1: %s\tChoice: %s" % (ip, grind_for_aspect(ip)))
    print ("IP2: %s\tChoice: %s" % (ip2, grind_for_aspect(ip2)))
    print ("IP3: %s\tChoice: %s" % (ip3, grind_for_aspect(ip3)))
    print ("IP4: %s\tChoice: %s" % (ip4, grind_for_aspect(ip4)))
    print ("IP5: %s\tChoice: %s" % (ip5, grind_for_aspect(ip5)))
    print ("IP6: %s\tChoice: %s" % (ip6, grind_for_aspect(ip6)))
    print ("IP7: %s\tChoice: %s" % (ip7, grind_for_aspect(ip7)))
    print ("IP8: %s\tChoice: %s" % (ip8, grind_for_aspect(ip8)))
    print ("IP9: %s\tChoice: %s" % (ip9, grind_for_aspect(ip9)))
    print ("IP10: %s\tChoice: %s" % (ip10, grind_for_aspect(ip10)))