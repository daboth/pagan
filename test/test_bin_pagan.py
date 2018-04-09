import os
from subprocess import PIPE
from subprocess import Popen


def test_simple_call():
    """check if calling the script simply works and yields no error"""
    p = Popen(["pagan", "--noshow", "--output=/tmp/0101010101.png", "0101"],
              stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    assert stdout
    assert not stderr


def test_simple_call_err():
    """fail if called with wrong arguments"""
    p = Popen(["pagan", "--output=/tmp/0101010101.png", "--err", "0101"],
              stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    assert not stdout
    assert stderr


def test_simple_call_err_no_input():
    """fail if no input given"""
    p = Popen(["pagan", "--output=/tmp/0101010101.png"],
              stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    assert not stdout
    assert stderr


def test_replace_chars_in_filename():
    """test replace chars in filename, if only called with input

    no punctuation allowed, so replace "one.png" with "one-png"
    """
    p = Popen(["pagan", "--noshow", "/tmp/one.png"],
              stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    assert not stderr
    assert stdout
    expected_filename = "-tmp-one-png.png"
    assert os.path.isfile(expected_filename)
    if os.path.isfile(expected_filename):
        os.unlink(expected_filename)
