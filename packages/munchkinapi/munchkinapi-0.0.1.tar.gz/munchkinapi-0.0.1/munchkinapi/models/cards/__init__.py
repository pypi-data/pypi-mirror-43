"""This module contains everything on the Card model, along with all the cards"""

from .base import Card, InvalidCardException
from .doors import ALL_DOOR_CARDS
from .treasures import ALL_TREASURE_CARDS


ALL_CARDS = {
    'treasures': ALL_TREASURE_CARDS,
    'doors': ALL_DOOR_CARDS
}


__all__ = ['ALL_CARDS']
