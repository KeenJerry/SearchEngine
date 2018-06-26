from django.shortcuts import render
from SearchEngine.tools import TrieTree
import os
import json
# Create your views here.

trie_tree = TrieTree()
tf_idf_tree = TrieTree()

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

if __name__ == "__main__":
    print('start build trie tree...')
    create_trie_tree(trie_tree, '../TermResource/pos0.json')
    print('start build tf_idf tree...')
    create_trie_tree(tf_idf_tree, '../TermResource/tf0.json')

    node = trie_tree.find_term('apple')
    i = 0



