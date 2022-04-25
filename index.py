from cmath import log, log10
from distutils.log import Log
import math
import re
import xml.etree.ElementTree as et  
from nltk.stem import PorterStemmer 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


class Index: 

    def __init__(self, file_path, titles_path, docs_path, words_path):
        self.STOP_WORDS = set(stopwords.words('english'))
        self.IDs_to_title = {}
        self.words_id_freq = {}
        self.nltk_test = PorterStemmer()
        self.word_to_id_to_tf = {}
        self.word_to_idf = {}
        self.word_to_doc_to_relevance = {}

        self.parse(file_path)

    def parse(self, input_file):
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()
        self.total_docs = len(wiki_xml_root)

        for wiki_page in wiki_xml_root:
            title: str = wiki_page.find("title").text
            pageID: int = int(wiki_page.find('id').text)
            self.IDs_to_title[pageID] = title

            page_text = wiki_page.find("text").text 
            tokenization_regex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
            page_tokens = re.findall(tokenization_regex, title + " " + page_text)
        
            aj = 0
            for word in page_tokens:
                if (word.lower() in self.STOP_WORDS):
                    continue
                word = self.nltk_test.stem(word)

                if word in self.words_id_freq:
                    if pageID in self.words_id_freq[word]:
                        self.words_id_freq[word][pageID] += 1
                        
                    else:
                        self.words_id_freq[word][pageID] = 1
                
                else:
                    if word not in self.words_id_freq:
                        self.words_id_freq[word] = {}
                    self.words_id_freq[word][pageID] = 1
                

                if self.words_id_freq[word][pageID] > aj:
                    aj = self.words_id_freq[word][pageID]

            for word in self.words_id_freq:
                if pageID in self.words_id_freq[word]:
                    if not word in self.word_to_id_to_tf:
                        self.word_to_id_to_tf[word] = {}
                    self.word_to_id_to_tf[word][pageID] = self.words_id_freq[word][pageID]/aj

                    if not word in self.word_to_idf:
                        self.word_to_idf[word] = 1
                    else: 
                        self.word_to_idf[word] += 1

        for word in self.word_to_idf:
            self.word_to_idf[word] = math.log(self.total_docs/self.word_to_idf[word])
        
            
    def relevance(self):
        # for word in self.word_to_id_to_tf:
        #     self.word_to_doc_to_relevance[word] = {}
        #     for pageID in self.word_to_id_to_tf[word]:
        #         self.word_to_doc_to_relevance[word][pageID] = self.word_to_idf[word]*self.word_to_id_to_tf[word][pageID]
            




        



