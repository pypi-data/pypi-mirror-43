"""This module contains the SportsDrink card"""
from .base import TreasureCard

class SportsDrinkCard(TreasureCard):
    """The Nasty tasting sports drink card"""
    name = 'Nasty tasting sports drink'
    second_type = 'one_shot'
    description = ''
    effects = []  # TreasureCard.incr_hp(5), ]
    # counter
