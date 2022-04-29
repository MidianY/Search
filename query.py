from file_io import *
from index import *
from nltk.stem import PorterStemmer 
import nltk
import sys
nltk.download('stopwords')
from nltk.corpus import stopwords

class Query:
    def __init__(self, title, doc_file, word_file, pageRank):
        self.ids_to_titles = {}
        self.ids_to_pageranks = {}
        self.words_to_doc_relevance = {}
        self.use_pagerank = pageRank
        read_title_file(title, self.ids_to_titles)
        read_docs_file(doc_file, self.ids_to_pageranks)
        read_words_file(word_file, self.words_to_doc_relevance)

    def get_query(self, inputs):
        page_id_to_relevance = {}
        input = inputs.split(" ")
        for word in input:
            if word not in stopwords:
                word_list = PorterStemmer.stem(word)

        if word_list[-1] == "--pagerank":
            for word in word_list[:-1]:
                for pageID in self.words_to_doc_relevance[word]:
                    if pageID not in page_id_to_relevance:
                        page_id_to_relevance[pageID] = 0
                page_id_to_relevance[pageID] += self.words_to_doc_relevance[word][pageID] + self.ids_to_pageranks[pageID]

        else:
            for word in word_list:
                for pageID in self.words_to_doc_relevance[word]:
                    if pageID not in page_id_to_relevance:
                        page_id_to_relevance[pageID] = 0
                    page_id_to_relevance[pageID] += self.words_to_doc_relevance[word][pageID]

        relevance = page_id_to_relevance.item().sort(reverse =True, key =self.my_function)
        
        n = 0
        while n < 10:
            print((n+1) + self.ids_to_titles[relevance[n][0]]) 
            n += 1

    def my_function(e):
        return e[1]
    
    def repl(self):
        while True:
            print(sys.argv)
            inputs = input("Enter an input: ")
            if inputs == ":quit":
                break
            print(self.get_query(inputs.lower()))
        

if __name__ == "__main__":
    use_pagerank = False

    if len(sys.argv) == 5 and sys.argv[1] == "--pagerank":
        query = Query(sys.argv[1], sys.argv[2], sys.argv[3], True)
        query.repl()
    
    else: 
        query = Query(sys.argv[1], sys.argv[2], sys.argv[3], False)
        query.repl()
   
    


        
            
    