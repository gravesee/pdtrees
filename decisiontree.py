import pprint
import numpy as np
from interaction import Interaction
from node import Node

class DecisionTree(object):
    """Decision tree class"""
    def __init__(self, df, attributes, target):
        self.df = df
        self.attributes = attributes
        self.target = target
        self.__root = Node(type='root')
        self.leaves = []
        self.support = None
    
    #Test program
    def induce(self, df=None, parent=None, side='root', depth=0):
        # var = raw_input("Press a key to step through")
        if df is None:
            df = self.df

        if parent is None:
            parent = self.__root

        # create base node
        node = Node(parent, depth=depth, cnt=len(df))
        
        # find best splits for all attribtues
        splits = self.get_splits(df, self.attributes, self.target)

        # check if a split exists, if so find best and split df
        found_split = np.any([s.has_split() for s in splits])
        if ((not found_split) | (depth >= 2)):
            node.type, node.side = ('leaf', side)
            self.leaves.append(node)
            return
        else:            
            # find attribute that best splits the data
            best_attr = self.get_max_split(splits)
            attr, val, pos, iv = best_attr.get_split()

            node.type, node.attr, node.val, node.side = ('node', attr, val, side)

            print "Splitting on %s" % attr
            left, right = self.split_df(df, best_attr)
            depth += 1
            self.induce(left , parent=node, side='left' , depth=depth)
            self.induce(right, parent=node, side='right', depth=depth)


    def get_splits(self, df, dict, y):
        """For list of attributes, find best split for each and return dict
           of results"""
        result = []
        #For each attribute find the split that maximizes IV
        for d in dict:
            attr, corr, mincnt = (d['attr'], d['corr'], d['mincnt'])

            try:
                i = Interaction(df[attr], df[y])
                split = i.split(mincnt, corr, verbose=False)
                result.append(split)
            except TypeError:
                pass
        return result

    def get_max_split(self, res):
        """Find best splitting attribute from dict of attribute splits"""
        attr = max(res, key=lambda split: split.iv)
        return attr

    def split_df(self, df, split):
        """Split df on best attr and return left and right dfs"""
        attr, val = split.attr, split.val
        return df[df[attr]<=val], df[df[attr]>val]

    def print_tree(self):
        for branch, leaf in enumerate(self.leaves):
            # for par in leaf.lineage:
            #     print "branch: %s par: %s" % (n, par.attr)
            leaf.translate(branch)
            # print "\nthen tree = %s\n" % n

    def calc_support(self):
        """function that calculates percent contribution of each attribute
           to branch.  Returns a dict of attributes for each branch"""
        pp = pprint.PrettyPrinter()

        support = []
        for branch, leaf in enumerate(self.leaves):
            support.append({})
            counts = np.array([n.cnt for n in leaf.lineage], dtype='float')[1:]
            total = sum(counts)
            for node in leaf.lineage[1:]:
                if node.type != 'root':
                    support[branch][node.parent.attr] = node.cnt / total
            print "Counts %s" % counts
        print "Calculating support:"
        pp.pprint(support)
        self.support = support