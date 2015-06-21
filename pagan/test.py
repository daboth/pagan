import ipgrinder
import pprint



aspects_found = []
weapons_found = []


def init_expected_weapon_list():
    twohand = ipgrinder.TWOHANDED_WEAPONS
    onehand = ipgrinder.ONEHANDED_WEAPONS
    shield = ipgrinder.SHIELDS

    dualwield_variations = []
    weapon_shield_variations = []

    for item in onehand:
        for i in onehand:
            dualwield_variations.append([item, i])
        for j in shield:
            weapon_shield_variations.append([j, item])

    return twohand + onehand + dualwield_variations + weapon_shield_variations


def test_ips():

    oct1 = 0
    oct2 = 0
    oct3 = 0
    oct4 = 0

    for i in range(256):
        for j in range(256):
            for k in range(256):
                for l in range(256):
                    ip = ("%r.%r.%r.%r" % (oct1, oct2, oct3, oct4))
                    aspect = ipgrinder.grind_for_aspect(ip)
                    weapon = ipgrinder.grindIpForWeapon(ip)
                    if aspect not in aspects_found:
                        aspects_found.append(aspect)

                    if weapon not in weapons_found:
                        weapons_found.append(weapon)
                    # if ([] in weapon):
                    #     print "WHAT? %r" % ip
                    oct4 +=1

                    #print ip
                oct3 += 1
                oct4 = 0
            oct2 += 1
            oct3 = 0
            print ("##########")
            print (ip)
            print ("Aspects: %r %r" % (len(aspects_found), aspects_found))
            print ("Weapons: %r %r" % (len(weapons_found), weapons_found))
        oct1 += 1
        oct2 = 0

    print ("All aspects found: %r", all_found)

if __name__ == "__main__":

    variations = init_expected_weapon_list()

    test_ips()

    all_found = False
    all_found2 = False

    print("All found weapons variations: %r" % variations)
    if sorted(aspects_found) == sorted(ipgrinder.ASPECTSTYLES):
        all_found = True
    if sorted(weapons_found) == sorted(variations):
        all_found = True

    print ("Found aspects: %r" % sorted(aspects_found))
    print ("Expected aspects: %r" % sorted(ipgrinder.ASPECTSTYLES))

    print ("Found weapon combinations: %r" % sorted(aspects_found))
    print ("Expected weapon combinations: %r" % sorted(ipgrinder.ASPECTSTYLES))


