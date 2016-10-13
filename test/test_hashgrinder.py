# -*- coding: latin-1 -*-
import pagan


def test_hashgrinder_asmain():
    # taken from pagan.hashgrinde.main

    # Testing some hashes.
    hash1 = "0396233d5b28eded8e34c1bf9dc80fae34756743594b9e5ae67f4f7d124d2e3d"
    hash2 = "ef101b0bc42f41e23e325f3da71daeff43ff7df9d41ff268e53a06c767de8487"
    hash3 = "ca4da36c48be1c0b87a7d575c73f6e42"

    pagan.hashgrinder.grind_hash_for_colors(hash1)
    pagan.hashgrinder.grind_hash_for_colors(hash2)
    pagan.hashgrinder.grind_hash_for_colors(hash3)

    pagan.hashgrinder.hex2rgb('#ffffff')
    pagan.hashgrinder.hex2rgb('#ffff00')
    pagan.hashgrinder.hex2rgb('#f5f5f5')
