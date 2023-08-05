"""This module contains the base Card class that all cards must inherit"""
from cerberus import Validator

from .schemas.card import CARD_SCHEMA


class Card:
    """The base card class that all of our cards finally inherit"""
    name = None
    main_type = None  # treasure / door
    second_type = None # monster / curse/ enhancer / class etc.
    effects = []
    schemas = [CARD_SCHEMA]
    errors = {}

    def json(self):
        """Provides a basic dictionary with all the data of the card"""
        return {
            'name': self.name,
            'main_type': self.main_type,
            'second_type': self.second_type
        }

    def validate(self):
        """Validates a card based on the provided schemas"""
        for schema in self.schemas:
            validator = Validator(schema, allow_unknown=True)
            if not validator.validate(self.json()):
                self.errors = validator.errors
                raise InvalidCardException(self.json(), validator.errors)


class InvalidCardException(Exception):
    """This exception is raised at card.validate()"""
