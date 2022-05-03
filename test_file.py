import pytest
from index import *
from query import *


def test_checklink():
    '''checking that this method can properly identify if something is a link '''
    index = Index("test_xml.xml", "titles.txt", "words.txt", "docs.txt")
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

    index = Index("test_xml.xml", "titles.txt", "words.txt", "docs.txt")
    id_to_title = {0: 'Welcome', 1: 'Hi Again', 2: 'Hi'}
    id_to_links = {1: {0}, 2: {1}}

    assert index.IDs_to_title == id_to_title
    assert index.id_to_linked_id == id_to_links
    assert len(index.words_id_freq) == 19

def test_page_rank():
    '''checking whether the pagerank calculation matches the values given'''

    index1 = Index("test2_xml.xml", "titles.txt", "words.txt", "docs.txt")
    index2 = Index("empty.xml", "titles.txt", "words.txt", "docs.txt")
    expected_page_rank_1 = {1: 0.4326427188659158, 
        2: 0.23402394780075067, 3: 0.33333333333333326}
    expected_page_rank_2 = {}

    assert index1.id_to_page_rank == expected_page_rank_1
    assert index2.id_to_page_rank == expected_page_rank_2
    


    






 




