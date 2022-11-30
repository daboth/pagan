# -*- coding: latin-1 -*-
import os

import pagan.generator as generator


class Avatar():

    # Default output path is in the current working directory.
    DEFAULT_OUTPUT_PATH = os.path.join(os.getcwd(), "output/")

    # Default filename.
    DEFAULT_FILENAME = ('pagan')

    # Default extension
    DEFAULT_EXTENSION = 'png'

    ALLOWED_EXTENSIONS = ['bmp', 'gif', 'png', 'tiff']

    DEFAULT_HASHFUN = generator.HASH_MD5

    def __init__(self, inpt, hashfun=DEFAULT_HASHFUN):
        """Initialize the avatar and creates the image."""
        self.img = self.__create_image(inpt, hashfun)

    def __create_image(self, inpt, hashfun):
        """Creates the avatar based on the input and
        the chosen hash function."""
        if hashfun not in generator.HASHES.keys():
            print ("Unknown or unsupported hash function. Using default: %s"
                   % self.DEFAULT_HASHFUN)
            algo = self.DEFAULT_HASHFUN
        else:
            algo = hashfun
        return generator.generate(inpt, algo)

    def show(self):
        """Shows a preview of the avatar in an external
        image viewer."""
        self.img.show()

    def change(self, inpt, hashfun=DEFAULT_HASHFUN):
        """Change the avatar by providing a new input.
        Uses the standard hash function if no one is given."""
        self.img = self.__create_image(inpt, hashfun)

    def save(self,
        path=DEFAULT_OUTPUT_PATH,
        filename=DEFAULT_FILENAME,
        extension=DEFAULT_EXTENSION):
        """Saves a avatar under the given output path to
        a given filename. The file ending ".png" is appended
        automatically. If the path does not exist, it will be
        created. When no parameters are omitted, a default path
        and/or filename will be used."""

        # Check if the extension is an allowed one
        if extension not in self.ALLOWED_EXTENSIONS:
            raise Exception(
                'Extension "%s" is not supported. Supported extensions are: %s'
                %(extension, ', '.join(self.ALLOWED_EXTENSIONS)))

        # Creates a path when it does not exist.
        if not os.path.exists(path):
            os.makedirs(path)

        # Make sure extension has no leading dot
        if extension.startswith('.'):
            extension = extension[1:]

        # Cut the file extension, if it's part of the filename.
        if filename[-len(extension):] == extension:
            filename = filename[:-len(extension)-1]

        # Saves the image under the given filepath.
        filepath = ('%s%s.%s' % (path, filename, extension))
        filepath = os.path.join(path, '%s.%s' % (filename, extension))
        # FIXIT: filepath without SUFFIX, print writes false filename
        print ('Saving: %s' % filepath)
        self.img.save(filepath, extension.upper())
