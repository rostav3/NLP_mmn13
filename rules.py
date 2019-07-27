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

    def update_tuple(self, tuple, count=1):
        if tuple not in self.rules_dictionary_counter:
            self.rules_dictionary_counter[tuple] = 0
        self.rules_dictionary_counter[tuple] += count

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

        for children in node.children:
            if node.tag != children.tag:
                self.insert_rule(node.tag, children.tag)
            self.build_grammar_from_tree(children)

    def clean_grammer(self):
        dictionary = copy.deepcopy(self.rules_dictionary)

        for parent in dictionary:
            while len(self.rules_dictionary[parent]) == 1 and self.rules_dictionary[iter(self.rules_dictionary[parent])] is not None:
                val = iter(self.rules_dictionary[parent])
                self.rules_dictionary[parent] = self.rules_dictionary[val]
                conut = self.remove_rule(parent, self.rules_dictionary[parent])
                self.insert_rule(parent, self.rules_dictionary[val], conut)



    def is_terminal(self, node):
        return len(node.children) == 0

    def handleSingleChild(self, node):
        while len(node.children) == 1 and len(node.children[0].children) > 0:
            node.children = node.children[0].children
        return node

    def binarization(self):
        dictionary = copy.deepcopy(self.rules_dictionary)
        c = copy.deepcopy(self.reverse_rules_dictionary)
        exist_none_binary = False
        for parent in dictionary:
            if len(dictionary[parent]) == 1 and dictionary[parent] != {None}:
                print (dictionary[parent])

            if len(dictionary[parent]) > 2:
                exist_none_binary = True
                self.handle_many_childs(dictionary[parent], parent)
        if exist_none_binary:
            self.binarization()

    def handle_many_childs(self, node, tag):
        num = 0
        past_key=new_key = None
        length = len(node)
        if length%2 != 0:
            print ("%s", node)
        for child in node:
            if child is not None:
                if num % 2 == 0 and num != length-1:
                    new_key = self.get_new_key(tag)
                    count = self.remove_rule(tag, child)
                    self.insert_rule(tag, new_key, count)
                    self.insert_rule(new_key, child, count)
                elif num % 2 == 0 and num == length-1:
                    past_key = new_key
                    new_key = self.get_new_key(tag)
                    count = self.remove_rule(tag, past_key)
                    self.insert_rule(new_key, past_key, count)
                    self.insert_rule(new_key, child, count)
                else:
                    count = self.remove_rule(tag, child)
                    self.insert_rule(tag, new_key, count)
                    self.insert_rule(new_key, child, count)
                num += 1

    def remove_rule(self, node, children):
        num = self.rules_dictionary_counter[(node, children)]
        self.rules_dictionary_counter[(node, children)] = 0
        self.reverse_rules_dictionary[children].remove(node)
        self.rules_dictionary[node].remove(children)
        return num

    def insert_rule(self, node, children, count=1):
        self.update_tags(children)
        self.update_tuple((node, children), count)
        self.update_rule(node, children)
        self.update_reverse_rule(node, children)

    def get_new_key(self, key):
        key = "%s_%d" % (key, self.count, )
        self.count += 1
        self.tags.add(key)
        return key

    def printGrammer(self):
        for rule in self.rules_dictionary:
            if len(self.rules_dictionary[rule]) < 2:
                print ("this is a tuple: %s , %s" % (rule, self.rules_dictionary[rule]))
