### v0.21
**Major update**

 * Modified pagan to generate hashes from arbitrary input strings.
 * Avatar creation is now fully based on a hash in hexadecimal form instead of IPv4 addresses.
 * Supports all hash algorithms that are included in pythons hashlib.
 * Can still process IPv4 addresses, they are also hashed now. Same applies for IPv6 addresses.
 * Features more colors. Each part of the gear is now painted uniquely due to the potential of hashes.

 **Minor changes**

 * Did some refactoring.
 * Added documentation.