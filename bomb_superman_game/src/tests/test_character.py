import pytest
from character import character

def test_character():
    test = character.Character()
    
    assert test.get_strength() == 1
    assert test.get_speed() == 10
    assert test.get_pos() == (0, 0)
