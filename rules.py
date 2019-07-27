import copy

class Grammar():
    def __init__(self):
        self.rules_dictionary_counter = dict()
        self.reverse_rules_dictionary = dict()
        self.rules_dictionary = dict()
        self.tags = {None}
        self.count = 1

    def update_tags(self, tag):
        self.tags.add(tag)

    def update_tuple(self, tuple):
        if tuple not in self.rules_dictionary_counter:
            self.rules_dictionary_counter[tuple] = 0
        self.rules_dictionary_counter[tuple] += 1

    def update_rule(self, node, child_node):
        if node not in self.rules_dictionary:
            self.rules_dictionary[node] = {child_node}
        else:
            self.rules_dictionary[node].add(child_node)

    def update_reverse_rule(self, node, child_node):
        if child_node not in self.rules_dictionary:
            self.reverse_rules_dictionary[child_node] = {node}
        else:
            self.reverse_rules_dictionary[child_node].add(node)

    def build_grammar_from_tree(self, node):
        self.update_tags(node.tag)

        # insert terminals
        if len(node.children) is 0:
            self.update_tuple((node.tag, None))
            self.update_rule(node.tag, None)

        node = self.handleSingleChild(node)
        for children in node.children:
            if node.tag != children.tag:
                self.insert_rule(node.tag, children.tag)
            self.build_grammar_from_tree(children)

    def handleSingleChild(self, node):
        while len(node.children) == 1 and len(node.children[0].children) > 0:
            node.children = node.children[0].children
        return node

    def binarization(self):
        dictionary = copy.deepcopy(self.rules_dictionary)
        c = copy.deepcopy(self.reverse_rules_dictionary)
        exist_none_binary = False
        for parent in dictionary:
            if len(dictionary[parent]) > 2:
                num = 0
                exist_none_binary = True
                for child in dictionary[parent]:
                    if child is not None:
                        if num % 2 is 0:
                            new_key = self.get_new_key(parent)
                        self.remove_rule(parent, child)
                        self.insert_rule(parent, new_key)
                        self.insert_rule(new_key, child)
                        num += 1
        if exist_none_binary:
            self.binarization()

    def remove_rule(self, node, children):
        self.rules_dictionary_counter[(node, children)] -= 1
        self.rules_dictionary[node].remove(children)
        self.reverse_rules_dictionary[children].remove(node)

    def insert_rule(self, node, children):
        self.update_tags(children)
        self.update_tuple((node, children))
        self.update_rule(node, children)
        self.update_reverse_rule(node, children)

    def get_new_key(self, key):
        key = "%s_%d" % (key, self.count, )
        self.count += 1
        self.tags.add(key)
        return key

    def printGrammer(self):
        for rule in self.rules_dictionary:
            print ("this is a tuple: %s , %s" % (rule, self.rules_dictionary[rule]))
