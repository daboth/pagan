import ipgrinder
import pprint
from multiprocessing import Pool, cpu_count
from pprint import pprint


def workerOne(argTpl):
	idx, lst = argTpl
	print("Number %d" %(idx))
	#print "Nope"
	# for i in range(int(1e6)):
	# 	x +=1
#	print (len(x))
	return len(lst)

liste = range(1000)

liste2 = range(40,800)

def chunkIt(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0
	while last < len(seq):
		out.append(seq[int(last): int(last+avg)])
		last += avg
	return out


cpucores = cpu_count()

joblist = chunkIt(liste2, cpucores)

a = [len(elem)+10 for elem in joblist]

# for idx, elem in enumerate(joblist):
# 	print(idx, len(elem))

#print(a)

#print([(idx, elem) for idx, elem in enumerate(joblist)])
#pprint(joblist)

poolboy = Pool(cpucores)

poolmap = poolboy.map_async(workerOne, [(idx, elem) for idx, elem in enumerate(joblist)])

results = poolmap.get()

print (results)



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

                    # INSERT WORKER JOB HERE

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


