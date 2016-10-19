# -*- coding: latin-1 -*-
import tempfile
import pagan


def test_create():
    img0 = pagan.Avatar("")
    img1 = pagan.Avatar("", 0)
    img2 = pagan.Avatar("", -111)
    img3 = pagan.Avatar("", None)
    assert img2.img == img3.img
    assert img0.img == img1.img


def test_diffrent_hash():
    img0 = pagan.Avatar("", 0)
    img1 = pagan.Avatar("", 1)
    assert img0.img != img1.img


def test_umlaute():
    img0 = pagan.Avatar("äöüÄÖÜß")
    img1 = pagan.Avatar("äöüÄÖÜß", 4)
    assert img0.img != img1.img


def test_show():
    """check only if error is raised"""
    img0 = pagan.Avatar("You rock!")
    img0.show()


def test_change():
    img0 = pagan.Avatar("1")
    img1 = pagan.Avatar("0")
    assert img0.img != img1.img
    img0.change("0")
    assert img0.img == img1.img


def test_save():
    img0 = pagan.Avatar("1")
    tmpdir = tempfile.gettempdir()
    tmpfile = tempfile.mkstemp(".png", dir=tmpdir)[1]
    img0.save("/", tmpfile)
    img0.save(tmpdir, tmpfile)
    tmpfile = tempfile.mkstemp("", dir=tmpdir)[1]
    img0.save("/", tmpfile)
    img0.save(tmpdir, tmpfile)


if __name__ == "__main__":
    test_create()
    test_diffrent_hash()
    test_umlaute()
    test_show()
    test_change()
    test_save()
