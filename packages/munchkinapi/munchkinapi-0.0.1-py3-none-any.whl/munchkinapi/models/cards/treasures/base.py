"""This module contains the TreasureCard class"""
from munchkinapi.models.cards.base import Card
from munchkinapi.models.cards.schemas.treasure_card import TREASURE_CARD_SCHEMA

class TreasureCard(Card):
    """All treasure cards must inherit this class"""
    main_type = 'treasure'
    schemas = Card.schemas + [TREASURE_CARD_SCHEMA]
