import copy


class Grammar:
    def __init__(self):
        self.rules_dictionary_counter = dict()
        self.reverse_rules_dictionary = dict()
        self.rules = dict()
        self.tags = set()
        self.terminal = set()
        self.count = 1

    def update_tags(self, tag):
        self.tags.add(tag)

    def update_tuple(self, tuple, count=1):
        if tuple not in self.rules_dictionary_counter:
            self.rules_dictionary_counter[tuple] = 0
        self.rules_dictionary_counter[tuple] += count

    def update_rule(self, node, child_node):
        if node not in self.rules:
            self.rules[node] = {child_node}
        else:
            self.rules[node].add(child_node)

    def update_reverse_rule(self, node, child_node):
        if child_node not in self.rules:
            self.reverse_rules_dictionary[child_node] = {node}
        else:
            self.reverse_rules_dictionary[child_node].add(node)

    def build_grammar_from_tree(self, node):
        self.update_tags(node.tag)
        if len(node.children) == 0:
            self.terminal.add(node.tag)
        for child in node.children:
            if node.tag != child.tag:
                self.insert_rule(node.tag, child.tag)
            self.build_grammar_from_tree(child)

    def clean_grammer(self):
        # dictionary = copy.deepcopy(self.rules_dictionary)
        # REMOVE SINGLES
        for parent in self.rules.keys():
            children = list(self.rules[parent])
            while len(children) == 1 and children[0] not in self.terminal:
                # self.rules[parent] = self.rules[children[0]]
                conut = self.remove_rule(parent, children[0])
                for child in self.rules[children[0]]:
                    self.insert_rule(parent, child, conut)
                children = list(self.rules[parent])

    def is_terminal(self, node):
        return len(node.children) == 0

    def handleSingleChild(self, node):
        while len(node.children) == 1 and len(node.children[0].children) > 0:
            node.children = node.children[0].children
        return node

    def binarization(self):
        dictionary = copy.deepcopy(self.rules)
        c = copy.deepcopy(self.reverse_rules_dictionary)
        exist_none_binary = False
        for parent in dictionary:
            if len(dictionary[parent]) == 1 and dictionary[parent] != {None}:
                print(dictionary[parent])

            if len(dictionary[parent]) > 2:
                exist_none_binary = True
                self.handle_many_childs(dictionary[parent], parent)
        if exist_none_binary:
            self.binarization()

    def handle_many_childs(self, node, tag):
        num = 0
        past_key = new_key = None
        length = len(node)
        if length % 2 != 0:
            print("%s", node)
        for child in node:
            if child is not None:
                if num % 2 == 0 and num != length - 1:
                    new_key = self.get_new_key(tag)
                    count = self.remove_rule(tag, child)
                    self.insert_rule(tag, new_key, count)
                    self.insert_rule(new_key, child, count)
                elif num % 2 == 0 and num == length - 1:
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

    def remove_rule(self, node, child):
        num = self.rules_dictionary_counter[(node, child)]
        self.rules_dictionary_counter[(node, child)] = 0
        self.reverse_rules_dictionary[child].remove(node)
        print(child)
        print(self.rules[node])
        self.rules[node].remove(child)
        return num

    def insert_rule(self, node, child, count=1):
        self.update_tags(child)
        self.update_tuple((node, child), count)
        self.update_rule(node, child)
        self.update_reverse_rule(node, child)

    def get_new_key(self, key):
        key = "%s_%d" % (key, self.count,)
        self.count += 1
        self.tags.add(key)
        return key

    def printGrammer(self):
        for rule in self.rules:
            if len(self.rules[rule]) < 2:
                print("this is a tuple: %s , %s" % (rule, self.rules[rule]))
