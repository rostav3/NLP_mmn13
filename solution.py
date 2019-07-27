'''

This source file is an empty solution file inheriting the required spec class for this assignmentself.
It also demonstrates one way of writing your parses to the required output file

See the spec that this class inherits, for the spec details

'''

import tree
from rules import Grammar
from spec import Spec

g = Grammar()
class Submission(Spec):

    def train(self, training_treebank_file='data/heb-ctrees.train'):
        ''' mock training function, learns nothing '''
        with open(training_treebank_file, 'r') as train_set:
            for sentence in train_set:
                sentence_tree = tree.Tree()
                sentence_tree.build_tree(sentence)
                g.build_grammar_from_tree(sentence_tree.head)
            g.CNF()
            g.printGrammer()

    def parse(self, sentence):
        ''' mock parsing function, returns a constant parse unrelated to the input sentence '''
        return '(TOP (S (VP (VB TM)) (NP (NNT MSE) (NP (H H) (NN HLWWIIH))) (yyDOT yyDOT)))'
    
    def write_parse(self, sentences, output_treebank_file='output/predicted.txt'):
        ''' function writing the parse to the output file '''
        with open(output_treebank_file, 'w') as f:
            for sentence in sentences:
                f.write(self.parse(sentence))
                f.write('\n')
