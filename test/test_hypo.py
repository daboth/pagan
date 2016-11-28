# -*- coding: latin-1 -*-
import pagan
from hypothesis import given
import hypothesis.strategies as st


@given(st.text(), st.integers())
def test_hypo(inpt, hashnr):
    img = pagan.Avatar(inpt, hashnr)
    assert (img.img)


if __name__ == "__main__":
    test_hypo()
