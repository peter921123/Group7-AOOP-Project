import pytest
from attribute import attribute

def test_attribute():
    test = attribute.Attribute(strength = 1, speed = 10)
    
    assert test.get_strength() == 1
    assert test.get_speed() == 10
    assert test.get_pos() == (0, 0)

    test.set_strength(5)
    test.set_speed(5)
    test.set_pos(5, 5)

    assert test.get_strength() == 5
    assert test.get_speed() == 5
    assert test.get_pos() == (5, 5)

    print(test.get_strength())
    print(test.get_speed())
    print(test.get_pos())
