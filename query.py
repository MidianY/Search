from file_io import *
from index import *
from nltk.stem import PorterStemmer 
import nltk
import sys
nltk.download('stopwords')
from nltk.corpus import stopwords

class Query:
    def __init__(self, pageRank, title, doc_file, word_file):
        self.ids_to_titles = {}
        self.ids_to_pageranks = {}
        self.words_to_doc_relevance = {}
        self.page_id_to_relevance = {}
        self.use_pagerank = pageRank
        self.nltk_test = PorterStemmer()
        read_title_file(title, self.ids_to_titles)
        read_docs_file(doc_file, self.ids_to_pageranks)
        read_words_file(word_file, self.words_to_doc_relevance)
        
        

    def find_score(self, word):
        if word in self.words_to_doc_relevance:
            for word in self.words_to_doc_relevance.keys():
                for pageid in self.words_to_doc_relevance[word]:
                    if pageid not in self.page_id_to_relevance:
                        self.page_id_to_relevance[pageid] = 0
                    self.page_id_to_relevance[pageid] += self.words_to_doc_relevance[word][pageid]
    
    def stem_words(self, word):
        if word.lower() in set(stopwords.words('english')):
            return ""
        return self.nltk_test.stem(word.lower())

    def get_query(self, query):
        split_input = query.split(" ")
        
        for word in split_input:
            words = self.stem_words(word)
            if words != "":
                self.find_score(words)
        
        all_id = list(self.page_id_to_relevance.keys())

        if self.use_pagerank:
            all_id.sort(reverse=True, key=lambda id: self.page_id_to_relevance[id] * self.ids_to_pageranks[id])
        else:
            all_id.sort(reverse=True, key=lambda id: self.page_id_to_relevance[id])
        
        if len(all_id) == 0:
            print("no results found")
        
        num_results = min(10, len(all_id))

        for i in range(num_results):
            print(self.ids_to_titles[all_id[i]])
    
    def repl(self):
        while True:
            #print(sys.argv)
            inputs = input("search: ")
            if inputs == ":quit":
                break
            self.get_query(inputs.lower())

if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--pagerank":
        page_rank = True
        query = Query(page_rank, sys.argv[2], sys.argv[3], sys.argv[4])
        query.repl()
    
    elif len(sys.argv) == 4: 
        page_rank = False 
        query = Query(page_rank, sys.argv[1], sys.argv[2], sys.argv[3])
        query.repl()
    else:
        print("wrong arguments, please try again")

            
    