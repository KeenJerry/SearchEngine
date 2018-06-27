from WebSearchEngin.similar_terms import get_the_most_similar_term
from nltk.corpus import wordnet as wn
import nltk
import re
import enchant
import ply.lex as lex
import ply.yacc as yacc
from WebSearchEngin import views
from SearchEngine.tools import TrieTree
import json
from WebSearchEngin import bool_lex_parse
import math
#import itertools

def similar_query(tokens):
    tagged = nltk.pos_tag(tokens,tagset='universal')
    suggest_terms = {}
    for (term,tag) in tagged:
        need_to_change = True
        if tag=="NOUN":
            pos = wn.NOUN
        elif tag=="VERB":
            pos = wn.VERB
        elif tag=="ADJ":
            pos = wn.ADJ
        elif tag=="ADV":
            pos = wn.ADV
        else:
            need_to_change = False
        if need_to_change:
            t = get_the_most_similar_term(term,pos)
            if t:
                suggest_terms[term] = t
    print(suggest_terms)

    '''suggest_queries = list()
    for l in itertools.product([0,1],repeat=len(tokens)):
        query = list()
        for i in range(0,len(l)):
            if l[i]==0:
                query.append(tokens[i])
            elif tokens[i] in suggest_terms:
                query.append(suggest_terms[tokens[i]])
            else:
                break
        if(len(query)==len(l)):
            suggest_queries.append(query)'''
    suggest_query = tokens + list(suggest_terms.values())
    return suggest_query


def wildcard_query(term_list,tokens):
    suggest_map = {}
    for token in tokens:
        if re.search('(\*|\?)',token):
            suggest_map[token] = list()
            pattern = token.replace("*",".*").replace("?",".")+("$")
            print(pattern)
            for term in term_list:
                if re.match(pattern,term):
                    suggest_map[token].append(term)
    print(suggest_map)
    return suggest_map


def find_wildcard_tokens(tokens,result):
    for token in tokens:
        if re.search('(\*|\?)',token):
            result.add(token)


def check_spelling(token): #only for debug
    d = enchant.Dict('en_US')
    if not d.check(token):
        print(d.suggest(token))


def bool_search(sentence): #only for debug
    result = bool_lex_parse.parser.parse(sentence)
    if result is None:
        print("Find nothing")
        return None
    else:
        for key in result:
            # print(key, end=' ')
            print(filename[int(key)])


def VSM_search(tokens): #only for debug
    doc_score = {}
    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    for token in tokens:

        index = tf_idf_tree.find_term(stemmer.stem(token)).index
        idf = math.log(10000 / index["-1"])
        for key in index.keys():
            if key == -1:
                continue
            wf_idf = (1 + math.log(index[key])) * idf
            if key not in doc_score.keys():
                doc_score[key] = wf_idf
            else:
                doc_score[key] += wf_idf
    sorted_doc = sorted(doc_score.items(), key=lambda d: d[1])

    for key in sorted_doc:
        print(filename[int(key[0])])
        # print(key)
    print(sorted_doc)
    return sorted_doc


def phase_search(sentence): #only for debug
    print("phase",sentence)
    return [1,2]


def make_query(sentence):
    if FLAG_PHRASE:
        if FLAG_WILDCARD or FLAG_BOOL:
            print("ERROR: Do not support this mode combination!")
    tokens = nltk.word_tokenize(sentence)

    wildcard_map = {}
    if FLAG_WILDCARD:
        wildcard_map = wildcard_query(term_list,tokens) # need the list of all terms

    for token in tokens:
        if token not in wildcard_map:
            if re.match('[a-zA-Z]+?$',token): # is a word
                if FLAG_BOOL and not re.match('(AND$)|(OR$)|(NOT$)',token): # not AND/OR/NOT
                    check_spelling(token) # need to write a function for it; it only needs to print a suggestion

    if FLAG_BOOL:
        query = ""
        for token in tokens:
            if token in wildcard_map:
                query += " ( "
                for index,term in enumerate(wildcard_map[token]):
                    if index==0:
                        query = query + " " + term
                    else:
                        query = query + " OR " + term
                query += " ) "
            else:
                query = query + " " + token

        file_list = bool_search(query) # need to write a function for it
    elif FLAG_PHRASE:
        file_list = phase_search(tokens)
    else:
        new_query = []
        for token in tokens:
            if token not in wildcard_map.keys():
                new_query.append(token)
        for terms in wildcard_map.values():
            new_query += terms
        file_list = VSM_search(new_query)
        if(len(file_list)<5):
            suggest_query = similar_query(new_query)
            file_list = VSM_search(suggest_query)

    return file_list

def find_term(term):
    return trie_tree.find_term(term)




term_list = ["apple","app","application","apolo","bppb","appnd"]
path_to_term = '../TermResource/pos0.json'
FLAG_WILDCARD = True
FLAG_BOOL = False
FLAG_PHRASE = False

trie_tree = TrieTree()
tf_idf_tree = TrieTree()
views.create_trie_tree(trie_tree, '../TermResource/pos0.json')
views.create_trie_tree(tf_idf_tree, '../TermResource/tf0.json')
a_file = open('../TermResource/filenames.json')
filename = json.load(a_file)
if __name__ == "__main__":
    file = open(path_to_term)

    dict = json.load(file)
    term_list = dict.keys()



    # fl = make_query(" ( love AND computer ) AND app*n OR B2B AND ANDE")
    bl = make_query("proces*")

