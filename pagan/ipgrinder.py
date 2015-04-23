max_digitsum = 255.0 * 4
max_digit = 255.0

weaponstyles = ['TWOHANDED', 'SHIELD_ONEHANDED', 'ONEHANDED', 'ONEHANDED_ONEHANDED']
TWOHANDED_WEAPONS = ['GREATSWORD', 'BIGHAMMER', 'GREATMACE', 'GREATAXE', 'STAFF']
ONEHANDED_WEAPONS = ['SWORD', 'HAMMER', 'AXE', 'MACE', 'DAGGER']
SHIELDS = ['LONGSHIELD', 'ROUNDSHIELD', 'BUCKLER', 'SHIELD']


def grindIpForColors(ip):
    octets = ip.split('.')
    rgb1 = (int(octets[0]), int(octets[1]), int(octets[2]))
    rgb2 = (int(octets[1]), int(octets[2]), int(octets[3]))
    rgb3 = (int(octets[2]), int(octets[3]), int(octets[0]))
    rgb4 = (int(octets[3]), int(octets[0]), int(octets[1]))

    return [rgb1, rgb2, rgb3, rgb4]


def grindIpForArmor(ip):
    digitsum = getDigitSum(ip)
    return null


def grindIpForBody(ip):
    return null


# Grinds the ip address for a weapon to draw on the pixelmap.
# Utilizes the last ip octet for maximum difference. This helps
# to get more different results due to the last octet being the most
# variant in local areas. 
def grindIpForWeapon(ip):
    digitsum = getDigitSum(ip)
    lastdigit = getLastOctet(ip)
    decision = mapDecision(max_digitsum, len(weaponstyles), digitsum)
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
    for i in range(len(weaponstyles)):
        if (i < decision):
            choice = weaponstyles[i]
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

    print ("IP1: %s\tChoice: %s" % (ip, grindIpForWeapon(ip)))
    print ("IP2: %s\tChoice: %s" % (ip2, grindIpForWeapon(ip2)))
    print ("IP3: %s\tChoice: %s" % (ip3, grindIpForWeapon(ip3)))
    print ("IP4: %s\tChoice: %s" % (ip4, grindIpForWeapon(ip4)))
    print ("IP5: %s\tChoice: %s" % (ip5, grindIpForWeapon(ip5)))
    print ("IP6: %s\tChoice: %s" % (ip6, grindIpForWeapon(ip6)))
    print ("IP7: %s\tChoice: %s" % (ip7, grindIpForWeapon(ip7)))
    print ("IP8: %s\tChoice: %s" % (ip8, grindIpForWeapon(ip8)))