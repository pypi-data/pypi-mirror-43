"""This module contains the DoorCard class"""
from munchkinapi.models.cards.base import Card
from munchkinapi.models.cards.schemas.door_card import DOOR_CARD_SCHEMA


class DoorCard(Card):
    """All door cards must inherit this class"""
    main_type = 'door'
    schemas = Card.schemas + [DOOR_CARD_SCHEMA]
