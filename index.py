import xml.etree.ElementTree as et  
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords


class Index: 

    def __init__(self, file_path, titles_path, docs_path, words_path):

        self.parse(file_path)

        self.IDs_to_title = {}
        self.parsed_words = {}


    def parse(self, input_file):
        wiki_tree = et.parse(input_file)
        wiki_xml_root = wiki_tree.getroot()
        for wiki_page in wiki_xml_root:
            title: str = wiki_page.find("title").text
            pageID: int = wiki_page.find('id').text
            self.IDs_to_title[pageID] = title

            page_text = wiki_page.find("text").text 
            tokenization_regex = r"\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+"
            page_tokens = re.findall(tokenization_regex, title + " " + page_text)
            STOP_WORDS = set(stopwords.words('english'))
            for word in page_tokens:
                if not (word in STOP_WORDS):
                    nltk_test = PorterStemmer()
                    self.parsed_words.add(nltk_test.stem(word))


                
                

            





