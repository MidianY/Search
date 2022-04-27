import pytest
from index import *


def test_checklink():
    '''checking that this method can properly identify if something is a link '''
    index = Index("test_xml.xml", "", "", "")
    link1 = "[[ss|aa]]"
    link2 = "[[s|a]"
    link3 = "[[aa dd]]"
    link4 = "[[]]"
    assert index.check_link(link1) == True
    assert index.check_link(link2) == False
    assert index.check_link(link3) == True
    assert index.check_link(link4) == False

def test_parsing():
    '''checking that the parsing method is correctly populating all of the nested dictionaries'''

    index = Index("test_xml.xml", "", "", "")
    id_to_title = {0: 'Welcome', 1: 'Hi Again', 2: 'Hi'}
    word_freq = {'welcom': {0: 1}, 'hello': {0: 1}, 'hi': {0: 1, 1: 2, 2: 1},
        'xml': {0: 1}, 'file': {0: 1}, 'nice': {0: 1}, 'wonder': {0: 1, 1: 1},
            'brought': {0: 1}, 'camp': {1: 1}, 'jump': {1: 1, 2: 1}, 'see': {1: 1},
                'ok': {1: 1},
                    'bye': {1: 1}}

    assert index.IDs_to_title == id_to_title
    assert index.words_id_freq == word_freq
    assert index.IDs_to_title[0] == 'Welcome'
    assert index.IDs_to_title[1] == 'Hi Again'
    assert index.IDs_to_title[2] == 'Hi'


