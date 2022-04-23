import re
import sys
import xml.etree.ElementTree as et  
from nltk.stem import PorterStemmer 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


class Index: 

    def __init__(self, file_path, titles_path, docs_path, words_path):
        self.IDs_to_title = {}
        self.words_id_freq = {}
        self.STOP_WORDS = set(stopwords.words('english'))
        self.nltk_test = PorterStemmer()
        self.parse(file_path)

    def parse(self, input_file):
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            title: str = wiki_page.find("title").text
            pageID: int = int(wiki_page.find('id').text)
            self.IDs_to_title[pageID] = title

            page_text = wiki_page.find("text").text 
            tokenization_regex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
            page_tokens = re.findall(tokenization_regex, title + " " + page_text)
        
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

                    term_frequency = {}
                    term_frequency[pageID] = 1
                    self.words_id_freq[word][pageID] = 1
        

#don't need to store the parsed words it takes up too much space we can already use our existing for loop




