"""This module contains the base card validation schema"""
CARD_SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'main_type': {
        'type': 'string',
        'required': True,
        'empty': False,
        'allowed': ['treasure', 'door']
    },
    'second_type': {
        'type': 'string',
        'required': True,
        'empty': False
    }  # values are allowed based on the main type
}
