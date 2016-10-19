from subprocess import PIPE
from subprocess import Popen


def test_simple_call():
    """check if calling the script simply works and yields no error"""
    p = Popen(["pagan", "--output=/tmp/0101010101.png", "0101"],
              stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    assert stdout
    assert not stderr


def test_simple_call_err():
    p = Popen(["pagan", "--output=/tmp/0101010101.png", "--err", "0101"],
              stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    assert not stdout
    assert stderr


def test_simple_call_err_no_input():
    p = Popen(["pagan", "--output=/tmp/0101010101.png"],
              stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    assert not stdout
    assert stderr
