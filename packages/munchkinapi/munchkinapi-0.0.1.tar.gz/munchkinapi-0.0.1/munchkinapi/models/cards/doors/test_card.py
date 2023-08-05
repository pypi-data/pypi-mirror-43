"""A test module with a test card"""
from .base import DoorCard


class TestDoorCard(DoorCard):
    """Just a test card"""

    name = 'just a test card'

    second_type = 'blahblah'
