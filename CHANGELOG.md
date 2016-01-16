### 0.3.3
**Major changes**

 * Implementing the Avatar class in pagan.py as the main accessor.
 * Overall restructure for an object oriented approach.
 * Avatar objects can now be instantiated and manipulated before drawing.
 * Hash functions can now be omitted on Avatar creation by using simple constants (e.g., pagan.SHA512).
 * Generator paths are now OS independent.

**Minor changes**

 * Comment cleanup on some methods.
 * Constants are now initialised in __init__.py

### 0.2.3
**Major changes**

 * Refactoring of the main filename from pagan.py to generator.py
 * Added pathhandling for correct template reading to import pagan as a installed module.

**Minor changes**

 * Hashfunction accessors are now stored in a dictionary.
 * When run as main, the predefined samples run all available hash algorithms.
 * Added a setup script and manifest to publish on pypi.

### 0.2.2
**Minor changes**

 * Refactoring
 * Cleanup

### 0.2.1
**Major changes**

 * Modified pagan to generate hashes from arbitrary input strings.
 * Avatar creation is now fully based on a hash in hexadecimal form instead of IPv4 addresses.
 * Supports all hash algorithms that are included in pythons hashlib.
 * Can still process IPv4 addresses, they are also hashed now. Same applies for IPv6 addresses.
 * Features more colors. Each part of the gear is now painted uniquely due to the potential of hashes.

**Minor changes**

 * Did some refactoring.
 * Added documentation.
