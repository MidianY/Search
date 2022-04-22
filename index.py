import re
import xml.etree.ElementTree as et  
from nltk.stem import PorterStemmer 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


class Index: 

    def __init__(self, file_path, titles_path, docs_path, words_path):
        self.IDs_to_title = {}
        self.parse(file_path)
        self.words_id_freq = {}
        #words->ID->accounts

    def parse(self, input_file):
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()

        for wiki_page in wiki_xml_root:
            parsed_words = []
            title: str = wiki_page.find("title").text
            pageID: int = wiki_page.find('id').text
            self.IDs_to_title[pageID] = title

            page_text = wiki_page.find("text").text 
            tokenization_regex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
            page_tokens = re.findall(tokenization_regex, title + " " + page_text)
            STOP_WORDS = set(stopwords.words('english'))

            for word in page_tokens:
                if not (word.lower() in STOP_WORDS):
                    nltk_test = PorterStemmer()
                    parsed_words.append(nltk_test.stem(word))

            for word in parsed_words:
                a_j = 0

                if word in self.words_id_freq:
                    if pageID in self.words_id_freq[word]:
                        self.words_id_freq[word][pageID] += 1
                    else:
                        self.words_id_freq[word][pageID] = 1
                else:
                    term_frequency = {}
                    term_frequency[pageID] = 1
                    self.words_id_freq[word][pageID] = term_frequency

    
    def tf_calculation(self):
        pass
                
                

            





