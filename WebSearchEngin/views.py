from django.shortcuts import render
from SearchEngine.tools import TrieTree
import os
import json
import nltk
from nltk.stem.snowball import SnowballStemmer
import enchant
import copy
import ply.lex as lex
import ply.yacc as yacc
# from query import similar_search, wildcard_search


def t_AND(t):
    r'AND'
    return t

def t_OR(t):
    r'OR'
    return t

def t_NOT(t):
    r'NOT'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_TK(t):
    r'[^ ]+'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_expression_binop(p):
    '''expression : expression AND expression
    | expression OR expression'''
    if p[2] == 'AND' : p[0] = AND(p[1], p[3])
    elif p[2] == 'OR' : p[0] = OR(p[1], p[3])

def p_expression_not(p):
    "expression : NOT expression"
    p[0] = p[2]

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]

def p_expression_token(p):
    "expression : TK"
    p[0] = trie_tree.find_term(p[1]).index

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


def sort_index(index):
    keys = index.keys()
    return sorted(keys)

def AND(index1, index2):
    index1_sort_keys = sort_index(index1)
    index2_sort_keys = sort_index(index2)

    result = []
    i = j = 0
    while i < len(index1_sort_keys) and j < len(index2_sort_keys):
        if index1_sort_keys[i] == index2_sort_keys[j]:
            result.append(index1_sort_keys[i])
            i = i + 1
            j = j + 1
        else:
            if index1_sort_keys[i] < index2_sort_keys[j]:
                i = i + 1
            else:
                j = j + 1
    return result

def OR(index1, index2):
    index1_sort_keys = sort_index(index1)
    index2_sort_keys = sort_index(index2)

    result = []
    i = j = 0
    while i < len(index1_sort_keys) or j < len(index2_sort_keys):
        if i < len(index1_sort_keys) and j < len(index2_sort_keys):
            if index1_sort_keys[i] == index2_sort_keys[j]:
                result.append(index1_sort_keys[i])
                # result.append(index2_sort_keys[j])
                i = i + 1
                j = j + 1
            else:
                if index1_sort_keys[i] < index2_sort_keys[j]:
                    result.append(index1_sort_keys[i])
                    i = i + 1
                else:
                    result.append(index2_sort_keys[j])
                    j = j + 1
        else:
            if i > len(index1_sort_keys) and j < len(index2_sort_keys):
                result.append(index2_sort_keys[j])
                j = j + 1
            else:
                result.append(index1_sort_keys[i])
                i = i + 1
    return result

def NOT(index1, index2):
    # index1_sort_keys = sort_index(index1)
    # index2_sort_keys = sort_index(index2)
    #
    # result = copy.deepcopy(index1_sort_keys)
    # i = j = 0
    # while i < len(index1_sort_keys) and j < len(index2_sort_keys):
    #     if index1_sort_keys[i] == index2_sort_keys[j]:
    #         result.remove(index1_sort_keys[i])
    #         i = i + 1
    #         j = j + 1
    #     else:
    #         if index1_sort_keys[i] < index2_sort_keys[j]:
    #             i = i + 1
    #         else:
    #             j = j + 1
    result = AND(index1, index2)
    new_result = copy.deepcopy(index1)
    keys = list(new_result)
    for key in keys:
        if key in result:
            new_result.pop(key)
    return new_result

def create_trie_tree(tree, path_to_term):
    file = open(path_to_term)
    dict = json.load(file)
    i = 0
    for key_term in dict:
        tree.add_term(key_term, index=dict[key_term])
        i = i + 1
        print('[', end='')
        for k in range(0, 50):
            if k * 867 <= i:
                print('+', end='')
            else:
                print(' ', end='')
        print(']')

def spell_correction(word):
    if not d.check(word):
        return d.suggest(word)[0]


# List of token names
tokens = (
    'TK',
    'AND',
    'OR',
    'NOT',
    'LPAREN',
    'RPAREN',
)

t_ignore = " \t"

# Build the lexer
lexer = lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
)

# Build the parser
parser = yacc.yacc()

# Create your views here.

trie_tree = TrieTree()
tf_idf_tree = TrieTree()
d = enchant.Dict('en_US')

def home():
    create_trie_tree(trie_tree, '../TermResource/pos0.json')
    create_trie_tree(tf_idf_tree, '../TermResource/tf0.json')

    # TODO get input

    while True:
        print('Please choose a search mode:')
        print('[1] Bool Search')
        print('[2] Similar Search')
        print('[3] Wildcard Search')
        flag = input()
        if flag == 1:
            print('You have chosed bool search.')
        if flag == 2:
            print('You have chosed similar search.')
        if flag == 3:
            print('You have chosed wildcard search.')

        # stemmer = SnowballStemmer("english")

        data = input('Please input your search statement:')

        if flag == 1:

            result = parser.parse(data)

            if result is None:
                print("Find nothing")
                return None
            else:
                for key in result:
                    print(key, end=' ')
                    # print(node1.index[key])

        if flag == 2:
            pass
            #similar_search(data)

        if flag == 3:
            pass
            term_list = ["apple", "app", "application", "apolo", "bppb", "appnd"]
            #wildcard_search(term_list, data)

# if __name__ == "__main__":
#      home()



