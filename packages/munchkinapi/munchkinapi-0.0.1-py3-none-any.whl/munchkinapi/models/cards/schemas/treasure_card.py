"""This module contains the treasure card validation schema"""
TREASURE_CARD_SCHEMA = {
    'main_type': {
        'type': 'string',
        'required': True,
        'empty': False,
        'allowed': ['treasure']}
}
