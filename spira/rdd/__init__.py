from .technology import TechnologyLibrary

global RULE_DECK_DATABASE
RULE_DECK_DATABASE = TechnologyLibrary('EMPTY')

def get_rule_deck():
    global RULE_DECK_DATABASE
    if RULE_DECK_DATABASE.name == 'EMPTY':
        initialize_default()
    return RULE_DECK_DATABASE

def initialize_default():
    from spira.technologies.default import purposes
    from spira.technologies.default import database
    
    # from spira.core.default import general
    # from spira.core.default import pdk_default