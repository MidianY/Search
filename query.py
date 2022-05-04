from file_io import *
from index import *
from nltk.stem import PorterStemmer 
import nltk
import sys
nltk.download('stopwords')
from nltk.corpus import stopwords

'''Query class handles user inputted query and produces up to the top 10 search results'''
class Query:
    def __init__(self, pageRank, title, doc_file, word_file):
        '''Query constructor
        Parameters:
        pageRank: a boolean. if true, reuslts will factor in pagerank
        title: a txt file of the page IDs corresponding to the titles in a wiki
        doc_file: a txt file of all the page IDs corresponign to their page rank
        word_file: a txt file of all the words corresponfig to the page IDs they appear in to the relevance score
        '''
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
        '''Method that populates page_id_to_relevance for a given word
        Parameters: 
        word : a processed string obtained from the query'''
        if word in self.words_to_doc_relevance:
            for pageid in self.words_to_doc_relevance[word]:
                if pageid not in self.page_id_to_relevance:
                    self.page_id_to_relevance[pageid] = 0
                self.page_id_to_relevance[pageid] += self.words_to_doc_relevance[word][pageid]
    
    def stem_words(self, word):
        '''Method that processes (stems, removes stop words, make lower case) each word in the query
        Paramters: word: a string obtained directly from the query'''
        if word.lower() in set(stopwords.words('english')):
            return ""
        return self.nltk_test.stem(word.lower())

    def get_query(self, query):
        '''Method that printd up to the top 10 most relevant titles for the given query
        Parameters: 
        query: the query as given by the user'''
        self.page_id_to_relevance = {}
        split_input = query.split(" ")
        for word in split_input:
            stemmed_word = self.stem_words(word)
            if stemmed_word  != "":
                self.find_score(stemmed_word)
        
        all_id = list(self.page_id_to_relevance.keys())

        if self.use_pagerank:
            all_id.sort(reverse=True, key=lambda id: (self.page_id_to_relevance[id] * self.ids_to_pageranks[id]))
        else:
            all_id.sort(reverse=True, key=lambda id: self.page_id_to_relevance[id])
        
        if len(all_id) == 0:
            print("no results found")
        
        num_results = min(10, len(all_id))

        for i in range(num_results):
            print(str(i+1) + " " + self.ids_to_titles[all_id[i]])
    
    def repl(self):
        '''The REPL that runs until user quits'''
        while True:
            inputs = input("search: ")
            if inputs == ":quit":
                break
            self.get_query(inputs.lower())
            

if __name__ == "__main__":
    '''Main method, instantiates query given sys args'''
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

            
    