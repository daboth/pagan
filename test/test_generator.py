import pagan
import pytest
import sys


def test_generate_by_hash():
    import hashlib
    md5 = hashlib.md5()
    inpt = ""
    if sys.version_info.major == 2:
        inpt = bytes(inpt)
    else:
        inpt = bytes(inpt, "utf-8")

    md5.update(inpt)
    img = pagan.generator.generate_by_hash(md5.hexdigest())
    assert img is not None
    img2 = pagan.generator.generate("", 0)
    assert img == img2

    with pytest.raises(pagan.generator.FalseHashError):
        img = pagan.generator.generate_by_hash(md5.hexdigest()[:2])

    with pytest.raises(pagan.generator.FalseHashError):
        img = pagan.generator.generate_by_hash(md5.hexdigest()+"A")
