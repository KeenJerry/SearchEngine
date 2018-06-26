
class TrieTree:

    def __init__(self):
        self.root = TrieNode()

    def add_term(self, term, file_name):
        node = self.root
        for char in term:
            for child in node.children:
                if char == child.char:
                    node = child
                    break
            new_node = TrieNode(char, file_name)
            node.children.append(new_node)
            node = new_node
        node.is_term = True

    def find_term(self, term):
        # TODO implement
        pass


class TrieNode:

    is_term = False
    char = None
    file_name = None
    children = []


    # TODO need more details

    def __init__(self, char, file_name):
        self.char = char
        self.file_name = file_name
