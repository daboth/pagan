import generator
import os

class Pagan():

    # Default output path is in the current working directory.
    DEFAULT_OUTPUT_PATH = ('%s/output/' % os.getcwd())
    # Default filename.
    DEFAULT_FILENAME = ('pagan')

    DEFAULT_HASHFUN = 'sha256'

    MD5 = generator.HASH_MD5
    SHA1 = generator.HASH_SHA1
    SHA224 = generator.HASH_SHA224
    SHA256 = generator.HASH_SHA256
    SHA384 = generator.HASH_SHA384
    SHA512 = generator.HASH_SHA512

    # Maps input parameters to match the
    # hash function in the generator.
    HASHES = {"md5" : MD5, "sha1" : SHA1, "sha224" : SHA224,
          "sha256" : SHA256, "sha384" : SHA384, "sha512" : SHA512}

    def __init__(self, inpt, hashfun=DEFAULT_HASHFUN):
        '''Initialize the paganicon and creates the image.'''
        self.img = self.__create_image(inpt, hashfun)

    def __create_image(self, inpt, hashfun):
        '''Creates the paganicon based on the input and
        the chosen hash function.'''

        try:
            algo = self.HASHES[hashfun]
        except KeyError:
            print ("Unknown or unsupported hash function. Using default: %s" % (self.DEFAULT_HASHFUN))
            algo = self.HASHES[self.DEFAULT_HASHFUN]

        return generator.generate(inpt, algo)

    def show(self):
        '''Shows a preview of the paganicon in an external
        image viewer.'''
        self.img.show()

    def save(self, path=DEFAULT_OUTPUT_PATH, filename=DEFAULT_FILENAME):
        '''Saves a paganicon under the given output path to
        a given filename. The file ending ".png" is appended
        automatically. If the path does not exist, it will be
        created. When no parameters are omitted, a default path
        and/or filename will be used.'''

        # Creates a path when it does not exist.
        if not os.path.exists(path):
            os.makedirs(path)
        # Saves the image under the given filepath.
        filepath = ("%s%s.png" % (path, filename))
        print ("Saving: %s" % filepath)
        self.img.save(filepath, 'PNG', transparency=0)