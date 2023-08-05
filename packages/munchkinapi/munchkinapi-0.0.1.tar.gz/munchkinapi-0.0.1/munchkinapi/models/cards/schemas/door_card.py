"""This module contains the base card validation schema"""

DOOR_CARD_SCHEMA = {
    'main_type': {
        'type': 'string',
        'required': True,
        'empty': False,
        'allowed': ['door']
    },
    'second_type': {
        'type': 'string',
        'required': True,
        'empty': False,
        'allowed': ['monster', 'class']
    }  # values are allowed based on the main type
}
