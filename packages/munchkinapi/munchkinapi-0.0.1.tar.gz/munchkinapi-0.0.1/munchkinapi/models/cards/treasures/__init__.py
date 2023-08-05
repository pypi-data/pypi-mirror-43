"""This module contains all the treasure cards"""
from munchkinapi.models.cards.utils import import_cards

from .base import TreasureCard


ALL_TREASURE_CARDS = import_cards(__file__, 'munchkinapi.models.cards.treasures', TreasureCard)


__all__ = ['ALL_TREASURE_CARDS']
