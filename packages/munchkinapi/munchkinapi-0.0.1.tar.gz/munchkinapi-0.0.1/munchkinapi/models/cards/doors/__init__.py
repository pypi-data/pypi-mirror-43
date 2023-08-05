"""This module contains all the door cards"""
from munchkinapi.models.cards.utils import import_cards

from .base import DoorCard


ALL_DOOR_CARDS = import_cards(__file__, 'munchkinapi.models.cards.doors', DoorCard)


__all__ = ['ALL_DOOR_CARDS']
