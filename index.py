import math
import re
import sys
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
        self.id_to_linked_id = {}
    
        self.parse(file_path)
        self.relevance_calculation()

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

            if page_text: #if the page exists
                page_tokens = re.findall(tokenization_regex, title + " " + page_text)

            aj = 0
            for word in page_tokens:
                #if the word is a stop word continue with the rest of the code
                if (word.lower() in self.STOP_WORDS):
                    continue

                #update the word to be the stemmed word to use in other loops 
                word = self.nltk_test.stem(word)

                #checking if it's a link
                if self.check_link(word):
                    link_text, link_title = self.split_link(word)


                    stem_word = self.nltk_test.stem(link_text[0])

                    # for linked_ID in self.IDs_to_title:
                    #     if self.IDs_to_title[linked_ID] == link_title:
                    #         if not pageID in self.id_to_linked_id:
                    #             self.id_to_linked_id[pageID] = set()
                    #         self.id_to_linked_id[pageID].add(linked_ID)

                    word = stem_word
                
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
    
    def check_link(self, word):
        #boolean that checks whether the word is a link
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

        # if ":" in stripped_word:
        #     list = stripped_word.split(":")
        #     return (re.findall(regex, list))
            

    def populate_word_to_id(self, word, pageID):
        
        

    def relevance_calculation(self):
        '''method that populates the idf dictionary by updating old values and
        calculates the corresponding relevance values using the idf and td dictionaaries'''

        for word in self.word_to_idf:
            self.word_to_idf[word] = math.log(self.total_docs/self.word_to_idf[word])
        
        for word in self.word_to_id_to_tf:
            self.word_to_doc_to_relevance[word] = {}
            for pageID in self.word_to_id_to_tf[word]:
                self.word_to_doc_to_relevance[word][pageID] = self.word_to_idf[word]*self.word_to_id_to_tf[word][pageID]

    def page_rank():
        pass

    def weight(self, k, j):
        pass


    # #main method
    # if __name__ == "main_":
    #     input = sys.argv
    #     print(input)
    #     file_path = "data"
    #     titles_path = input[1]
    #     docs_path = input[2]
    #     words_path = input[3]
    #     aClass = Index(file_path, titles_path, docs_path, words_path)


    
        



        
            




        



