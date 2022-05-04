import pytest
import nltk
nltk.download('stopwords')
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

def test_spltlink():
   '''checking that this method can properly split a link'''
   index = Index("test_xml.xml", "titles.txt", "words.txt", "docs.txt")
   link1 = "[[ss|hi i am a link]]"
   link2 = "[[aa|dd]]"
   assert index.split_link(link1) == (['hi', 'i', 'am', 'a', 'link'], 'ss')
   assert index.split_link(link2) == (['dd'], 'aa')

def test_parsing():
   '''checking that the parsing method is correctly populating all of the nested dictionaries
   we hand calculated all of these as it is a small xml file'''
 
   index = Index("test_xml.xml", "titles.txt", "words.txt", "docs.txt")
   id_to_title = {0: 'Welcome', 1: 'Hi Again', 2: 'Hi'}
   id_to_links = {1: {0}, 2: {1}}

   words_id_freq = {'welcom': {0: 1}, 'hello': {0: 1},
    'hi': {0: 1, 1: 2, 2: 1}, 'xml': {0: 1}, 'file': {0: 1},
    'nice': {0: 1}, 'wonder': {0: 1, 1: 1},'brought': {0: 1},
    'hope': {0: 1}, 'eat': {0: 1}, 'well': {0: 1}, 'come': {0: 1},
    'camp': {1: 1}, 'jump': {1: 1, 2: 1}, 'see': {1: 1}, 'ok': {1: 1},
    'bye': {1: 1}, 'excit': {1: 1}, 'thank': {1: 1}}

   word_to_id_to_tf = {'welcom': {0: 1.0}, 'hello': {0: 1.0},
    'hi': {0: 1.0, 1: 1.0, 2: 1.0}, 'xml': {0: 1.0},
    'file': {0: 1.0},'nice': {0: 1.0}, 'wonder': {0: 1.0, 1: 0.5},
    'brought': {0: 1.0}, 'hope': {0: 1.0}, 'eat': {0: 1.0},
    'well': {0: 1.0}, 'come': {0: 1.0}, 'camp': {1: 0.5}, 'jump': {1: 0.5, 2: 1.0},
    'see': {1: 0.5}, 'ok': {1: 0.5}, 'bye': {1: 0.5}, 'excit': {1: 0.5},
    'thank': {1: 0.5}}

   word_to_idf = {'welcom': 1.0986122886681098,
    'hello': 1.0986122886681098,
    'hi': 0.0,
    'xml': 1.0986122886681098,
    'file': 1.0986122886681098,
    'nice': 1.0986122886681098,
    'wonder': 0.4054651081081644,
    'brought': 1.0986122886681098,
    'hope': 1.0986122886681098,
    'eat': 1.0986122886681098,
    'well': 1.0986122886681098,
    'come': 1.0986122886681098,
    'camp': 1.0986122886681098,
    'jump': 0.4054651081081644,
    'see': 1.0986122886681098,
    'ok': 1.0986122886681098,
    'bye': 1.0986122886681098,
    'excit': 1.0986122886681098,
    'thank': 1.0986122886681098}

   word_to_doc_to_relevance = {'welcom': {0: 1.0986122886681098},
    'hello': {0: 1.0986122886681098},
    'hi': {0: 0.0, 1: 0.0, 2: 0.0},
    'xml': {0: 1.0986122886681098},
    'file': {0: 1.0986122886681098},
    'nice': {0: 1.0986122886681098},
    'wonder': {0: 0.4054651081081644, 1: 0.2027325540540822},
    'brought': {0: 1.0986122886681098},
    'hope': {0: 1.0986122886681098},
    'eat': {0: 1.0986122886681098},
    'well': {0: 1.0986122886681098},
    'come': {0: 1.0986122886681098},
    'camp': {1: 0.5493061443340549},
    'jump': {1: 0.2027325540540822, 2: 0.4054651081081644},
    'see': {1: 0.5493061443340549},
    'ok': {1: 0.5493061443340549},
    'bye': {1: 0.5493061443340549},
    'excit': {1: 0.5493061443340549},
    'thank': {1: 0.5493061443340549}}

   id_to_page_rank = {0: 0.3879107424975632, 
   1: 0.39722719194097234, 2: 0.21486206556146434}
 
   assert index.IDs_to_title == id_to_title
   assert index.id_to_linked_id == id_to_links
   assert len(index.words_id_freq) == 19
   assert index.words_id_freq == words_id_freq
   assert index.word_to_id_to_tf == word_to_id_to_tf
   assert index.word_to_idf == word_to_idf
   assert index.word_to_doc_to_relevance == word_to_doc_to_relevance
   assert index.id_to_page_rank == id_to_page_rank
   assert math.isclose(1, sum(index.id_to_page_rank.values()))


def test_process():
   '''checks whether the words are tokenised, stemmed, and stop words are removed correctly'''
   index = Index("test_xml.xml", "titles.txt", "words.txt", "docs.txt")
   assert index.process("stopping") == "stop"
   assert index.process("weLcOmE") == 'welcom'
   assert index.process("the") == ""
   assert index.process("WONDERFUL") == "wonder"
   assert index.process("") == ""

def test_page_rank():
    '''checking whether the pagerank calculation matches the values given from google drive'''
    
    index1 = Index("test2_xml.xml", "titles.txt", "words.txt", "docs.txt")
    index2 = Index("empty.xml", "titles.txt", "words.txt", "docs.txt")
    expected_page_rank_1 = {1: 0.4326427188659158, 
        2: 0.23402394780075067, 3: 0.33333333333333326}
    expected_page_rank_2 = {}
    assert index1.id_to_page_rank == expected_page_rank_1
    assert math.isclose(1, sum(index1.id_to_page_rank.values()))
    assert index2.id_to_page_rank == expected_page_rank_2

def test_stem_query():
   '''tests that the query string is correctly processed (stop words removed, lowercase, tokenized'''
   
   query = Query("test_xml.xml", "titles.txt", "words.txt", "docs.txt")
   assert query.stem_words("wonderful") == "wonder"
   assert query.stem_words("IS") == ""
   assert query.stem_words("stopping") == "stop"
   assert query.stem_words("QUERY") == "queri"
     


    


    






 




