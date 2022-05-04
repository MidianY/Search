import math
import re
import sys
from file_io import *
import xml.etree.ElementTree as et  
from nltk.stem import PorterStemmer 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import numpy as np 


class Index:
    def __init__(self, file_path, titles_path, docs_path, words_path):
        self.STOP_WORDS = set(stopwords.words('english'))
        self.IDs_to_title = {}
        self.words_id_freq = {}
        self.nltk_test = PorterStemmer()
        self.word_to_id_to_tf = {}
        self.word_to_idf = {}
        self.word_to_doc_to_relevance = {}
        self.id_to_linked_id = {}
        self.id_to_page_rank = {}
        self.parse(file_path)
        self.relevance_calculation()
        self.page_rank()
        write_title_file(titles_path, self.IDs_to_title)
        write_docs_file(docs_path, self.id_to_page_rank)
        write_words_file(words_path, self.word_to_doc_to_relevance)

    def parse(self, input_file):
        '''
        Parameters:

        Returns: it doesn't return anthing but populates dictionaries 
        '''
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()
        self.total_docs = len(wiki_xml_root)

        for wiki_page in wiki_xml_root:
            title: str = wiki_page.find("title").text
            pageID: int = int(wiki_page.find('id').text)
            self.IDs_to_title[pageID] = title.strip()

            page_text = wiki_page.find("text").text 
            tokenization_regex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"

            if page_text: #if the page exists
                page_tokens = re.findall(tokenization_regex, title + " " + page_text)

            aj = 0
            for word in page_tokens:
                
                #checking if it's a link
                if self.check_link(word):
                    link_text, link_title = self.split_link(word)

                    for linked_ID in self.IDs_to_title:
                        if self.IDs_to_title[linked_ID] == link_title:
                            if not pageID in self.id_to_linked_id:
                                self.id_to_linked_id[pageID] = set()
                            self.id_to_linked_id[pageID].add(linked_ID)

                    for text in link_text:
                        text = self.process(text)
                        if text == "":
                            continue
                        aj = self.populate_word_to_id(text, pageID, aj)

                else:
                    word = self.process(word)
                    if word == "":
                        continue
                    aj = self.populate_word_to_id(word, pageID, aj)
                
            self.tf_idf(pageID, aj)
    
    def process(self, word):
        '''
        Method handles processing words by making it lowercase, stemming, and 
        removing stopwords

        Parameters: a word/phase 
        
        Returns: the word or phrase after it is stemmed, stop words are removed,
        and lowercase'''

        lower_case = word.lower()
        if lower_case in self.STOP_WORDS:
            return ""
        return self.nltk_test.stem(lower_case)

    def check_link(self, word):
        '''method checks whether a word is a link
        Parameters: a word
        
        Returns: a boolean that checks whether the word is a link'''
      
        link_regex = '''\[\[[^\[]+?\]\]'''
        return bool(re.match(link_regex, word))
    
    def split_link(self, word):
        regex = r"[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
        stripped_word = word[2:-2]

        text = stripped_word
        title = stripped_word

        if "|" in stripped_word:
            list = stripped_word.split("|", 1)
            title = list[0]
            text = list[1]

        return (re.findall(regex,text), title.strip())

    def populate_word_to_id(self, word, pageID, aj):
        if word in self.words_id_freq:
            if pageID in self.words_id_freq[word]:
                self.words_id_freq[word][pageID] += 1        
            else:
                self.words_id_freq[word][pageID] = 1
        else:
            self.words_id_freq[word] = {}
            self.words_id_freq[word][pageID] = 1

        if self.words_id_freq[word][pageID] > aj:
            aj = self.words_id_freq[word][pageID]
        return aj
            
    def tf_idf(self, pageID, aj):

        #populating the tf dictionary
        for word in self.words_id_freq:
            if pageID in self.words_id_freq[word]:
                if not word in self.word_to_id_to_tf:
                    self.word_to_id_to_tf[word] = {}
                self.word_to_id_to_tf[word][pageID] = self.words_id_freq[word][pageID]/aj

                #initially setting the idf to the number of times the word appears in all the documents 
                if not word in self.word_to_idf:
                    self.word_to_idf[word] = 1
                else: 
                    self.word_to_idf[word] += 1

    def relevance_calculation(self):
        '''method that populates the idf dictionary by updating old values and
        calculates the corresponding relevance values using the idf and td dictionaaries'''

        for word in self.word_to_idf:
            self.word_to_idf[word] = math.log(self.total_docs/self.word_to_idf[word])

        for word in self.word_to_id_to_tf:
            self.word_to_doc_to_relevance[word] = {}
            for pageID in self.word_to_id_to_tf[word]:
                self.word_to_doc_to_relevance[word][pageID] = self.word_to_idf[word]*self.word_to_id_to_tf[word][pageID]

    def weight(self, k, j):
        e = 0.15
        n = len(self.IDs_to_title)
    
        if k == j:
            return e/n
        elif k not in self.id_to_linked_id:
            print(self.id_to_linked_id)
            return (e/n) + (1-e)*(1/(n-1))
        elif j in self.id_to_linked_id[k]:
            return (e/n) + (1-e)*(1/(len(self.id_to_linked_id[k])))
        else:
            return e/n

    def distance(self, old_r, new_r):
        sum = 0
        for id in old_r:
            sum += math.pow(new_r[id]-old_r[id], 2)
        return bool(math.sqrt(sum) > 0.001)

    def page_rank(self):
        r = {}
        #r prime is going to be our id to page rank dicrionary 

        for x in self.IDs_to_title.keys():
            r[x] = 0
            self.id_to_page_rank[x] = 1/len(self.IDs_to_title)
        
        while self.distance(r, self.id_to_page_rank):
            r = self.id_to_page_rank.copy()

            for j in self.IDs_to_title.keys():
                self.id_to_page_rank[j] = 0
                for k in self.IDs_to_title.keys():
                    self.id_to_page_rank[j] = self.id_to_page_rank[j] + (self.weight(k,j)*r[k]) 
            
if __name__ == "__main__":
    input = sys.argv
    wiki_data = input[1]
    title_path = input[2]
    docs_path = input[3]
    words_path = input[4]
    Index(wiki_data, title_path, docs_path, words_path)




        



