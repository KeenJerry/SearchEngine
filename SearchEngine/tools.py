
class TrieTree():

    def __init__(self):
        self.root = TrieNode()

    def add_term(self, term, index):
        node = self.root
        for char in term:
            child = self.find_char(node, char)
            if not child:
                new_child = TrieNode()
                new_child.char = char
                node.children.append(new_child)
                node = new_child
            else:
                node = child
        node.is_term = True
        node.index = index

    def find_char(self, node, char):
        for child in node.children:
            if child.char == char:
                return child
        return False

    def find_term(self, term):
        # TODO implement
        node = self.root
        # print(term)
        for char in term:
            child = self.find_char(node, char)
            node = child

        if not node.is_term:
            return None
        else:
            return node


class TrieNode:

    is_term = False
    char = None
    children = None
    index = None

    def __init__(self):
        self.children = []



