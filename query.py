from WebSearchEngin.similar_terms import get_the_most_similar_term, get_similar_terms
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
# from doc_analyzer import
#import itertools

def print_content(filename, path_to_file, sentence):
    new_filename = path_to_file + filename[14:]
    file = open(new_filename)
    content = file.read()
    # print(content)



def find_token_in_file(content):
    tokens = nltk.word_tokenize(content)
    # print(tokens)
    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    # print(stemmed_tokens)
    result_tokens = []
    for token in stemmed_tokens:
        if re.search('(\D/|/\D)', token):
            for tk in re.split('(/)', token):
                result_tokens.append(tk)
        else:
            result_tokens.append(token)


def similar_query(tokens):
    tagged = nltk.pos_tag(tokens,tagset='universal')
    weights = [ 1 for token in tokens ]
    suggest_terms = tokens
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
            dic = get_similar_terms(term,pos)
            if dic:
                for t,w in dic.items():
                    suggest_terms.append(t)
                    weights.append(w)
    print(suggest_terms,weights)
    return [suggest_terms,weights]


def wildcard_query(term_list,tokens):
    suggest_map = {}
    for token in tokens:
        if re.search('(\*|\?)',token):
            suggest_map[token] = list()
            pattern = token.replace("*",".*").replace("?",".")+("$")
            # print(pattern)
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
        return d.suggest(token)
    else:
        return []



def bool_search(sentence): #only for debug
    result = bool_lex_parse.parser.parse(sentence)
    if result is None:
        print("Find nothing")
        return None
    else:
        for key in result:
            # print(key, end=' ')
            print(filename[int(key)])
            # print_content(filename[int(key)], '../../reuters/Reuters/', sentence)


def VSM_search(tokens, weights): #only for debug
    doc_score = {}
    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    for id,token in enumerate(tokens):
        p = tf_idf_tree.find_term(stemmer.stem(token))
        if not p:
            print('Not find.')
            continue
        else:
            index = p.index
        idf = math.log(10000 / index["-1"])
        for key in index.keys():
            if key == -1:
                continue
            wf_idf = (1 + math.log(index[key])) * idf
            if key not in doc_score.keys():
                doc_score[key] = wf_idf * weights[id]
            else:
                doc_score[key] += wf_idf
    sorted_doc = sorted(doc_score.items(), key=lambda d: d[1])

    for key in sorted_doc:
        print(filename[int(key[0])])
        # print(key)
    # print(sorted_doc)
    return sorted_doc


def find_phase(index1, index2):
    index1_sort_keys = views.sort_index(index1)
    index2_sort_keys = views.sort_index(index2)

    result = []
    i = j = 0
    while i < len(index1_sort_keys) and j < len(index2_sort_keys):
        if index1_sort_keys[i] == index2_sort_keys[j]:
            for pos in index1[index1_sort_keys[i]]:
                if pos + 1 in index2[index2_sort_keys[j]]:
                    result.append(index1_sort_keys[i])
            # result.append(index1_sort_keys[i])
            i = i + 1
            j = j + 1
        else:
            if index1_sort_keys[i] < index2_sort_keys[j]:
                i = i + 1
            else:
                j = j + 1
    return result


def phase_search(sentence): #only for debug
    # tokens = sentence.split(' ')
    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    p1 = trie_tree.find_term(stemmer.stem(sentence[0]))
    p2 = trie_tree.find_term(stemmer.stem(sentence[1]))

    result = find_phase(p1.index, p2.index)

    if result is None:
        print("Find nothing")
        return None
    else:
        for key in result:
            # print(key, end=' ')
            print(filename[int(key)])
            # file = open(filename[int(key)])
            # content = file.read()


    return [1,2]


def make_query(sentence):
    if FLAG_PHRASE:
        if FLAG_WILDCARD or FLAG_BOOL:
            print("ERROR: Do not support this mode combination!")
    tokens = nltk.word_tokenize(sentence)

    wildcard_map = {}
    if FLAG_WILDCARD:
        wildcard_map = wildcard_query(term_list,tokens) # need the list of all terms
    tokens_added = []
    for token in tokens:
        if token not in wildcard_map:
            if re.match('[a-zA-Z]+?$',token): # is a word
                if FLAG_BOOL and re.match('(AND$)|(OR$)|(NOT$)',token): # not AND/OR/NOT
                    continue
                tokens_added = check_spelling(token) # need to write a function for it; it only needs to print a
                tokens = tokens + tokens_added
                # suggestion

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
    elif FLAG_SYNONYM:
        new_query = []

        for token in tokens:
            if token not in wildcard_map.keys():
                new_query.append(token)
        for terms in wildcard_map.values():
            new_query += terms
        suggest_query,weights = similar_query(new_query)
        file_list = VSM_search(suggest_query,weights)
    else:
        new_query = []

        for token in tokens:
            if token not in wildcard_map.keys():
                new_query.append(token)
        for terms in wildcard_map.values():
            new_query += terms
        file_list = VSM_search(new_query,[1 for q in new_query])
        if(len(file_list)<5):
            suggest_query,weights = similar_query(new_query)
            file_list = VSM_search(suggest_query,weights)

    return file_list

def find_term(term):
    return trie_tree.find_term(term)




term_list = ["apple","app","application","apolo","bppb","appnd"]
all = {}
for i in range(0, 10788):
    all[i] = '0'
path_to_term = './TermResource/pos0.json'
FLAG_WILDCARD = False
FLAG_BOOL = True
FLAG_PHRASE = False
FLAG_SYNONYM = False

trie_tree = TrieTree()
tf_idf_tree = TrieTree()
views.create_trie_tree(trie_tree, './TermResource/pos0.json')
views.create_trie_tree(tf_idf_tree, './TermResource/tf0.json')
a_file = open('./TermResource/filenames.json')
filename = json.load(a_file)
data = None
if __name__ == "__main__":
    file = open(path_to_term)

    dict = json.load(file)
    term_list = dict.keys()

    k = True

    while k:
        print('Please select a search method:')
        print('[1] Bool Search')
        print('[2] Phrase Search')
        print('[3] VSM Search')
        print('[4] Synonym Search')
        print('[5] Exit')

        flag = int(input())
        if flag == 1:
            FLAG_BOOL = True
            FLAG_PHRASE = False
            FLAG_WILDCARD = False
            FLAG_SYNONYM = False
        if flag == 2:
            FLAG_BOOL = False
            FLAG_WILDCARD = False
            FLAG_PHRASE = True
            FLAG_SYNONYM = False
        if flag == 3:
            FLAG_WILDCARD = True
            FLAG_PHRASE = False
            FLAG_BOOL = False
            FLAG_SYNONYM = False
        if flag == 4:
            FLAG_SYNONYM = True
            FLAG_BOOL = False
            FLAG_PHRASE = False
            FLAG_WILDCARD = False
        if flag == 5:
            k = False

        if k == True:
            data = input("Please enter your search statement:")
            # fl = make_query(" ( love AND computer ) AND app*n OR B2B AND ANDE")
            bl = make_query(data)

