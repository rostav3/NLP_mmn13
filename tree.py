class Node(object):
    def __init__(self, tag, parent):
        self.tag = tag
        self.children = []
        self.parent = parent
    def empty(self):
        if len(self.children) == 0:
            return True
        return False

    def add_children(self, node):
        self.children.append(node)

class Tree(object):
    def __init__(self, head=None):
        self.head = head

    def create_node(self, word, parent):
        node = Node(tag=word.replace(")", ""), parent=parent)
        if parent is not None:
            parent.add_children(node)
        return node

    def handle_node(self, word, parent):
        if word == "":
            return None
        if word.count(')') >= 1:
            words = word.split(" ")
            if len(words) == 1:
                node = self.create_node(word.replace(")", ""), parent).parent
                while word.count(')') != 0:
                    word = word[:-1]
                    if node is not None:
                        node = node.parent
                return node
            else:
                node = self.handle_node(words[0], parent)
                return self.handle_node(words[1].replace(" ", "").replace("\n", ""), node)

        word = word.replace(" ", "")
        node = self.create_node(word, parent)
        return node

    def build_tree(self, sentence):
        words = sentence.split("(")
        node = None

        for word in words:
            new_node = self.handle_node(word, node)
            if node is None and new_node is not None:
                self.head = new_node
            node = new_node
        return self

