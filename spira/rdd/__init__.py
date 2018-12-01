from .technology import TechnologyLibrary

global RULE_DECK
RULE_DECK = TechnologyLibrary('Empty Rule Deck')

def get_rule_deck():
    global RULE_DECK
    if RULE_DECK.name == 'Empty Rule Deck':
        initialize_default()
    return RULE_DECK

def initialize_default():
    return