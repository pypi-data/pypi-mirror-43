"""A second module with a second test card"""
from .base import DoorCard


class TestDoorCard2(DoorCard):
    """A second test card"""
    name = 'just a new test card'

    second_type = 'blahblah'
