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
        self.maxdepth = 3
        self.tree = {}
    
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
        if ((not found_split) | (depth >= self.maxdepth)):
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

    def build_tree(self):
        # induce the decision tree
        self.induce()
        
        # fill out dict with leaf nodes and branch ids
        for leaf in self.leaves:
            branch = leaf.get_branch(self.maxdepth)
            self.tree[branch] = {'leaf'   :leaf,
                                 'support':leaf.calc_support()}

    def print_tree(self):
        branches = sorted(self.tree.keys())

        for branch in branches:
            self.tree[branch]['leaf'].translate(branch)
            # print leaf.get_branch(self.maxdepth)

    # def calc_support(self):
    #     """function that calculates percent contribution of each attribute
    #        in branch.  Returns a dict of attributes for each branch"""
    #     pp = pprint.PrettyPrinter()

    #     support = []
    #     for branch, leaf in enumerate(self.leaves):
    #         support.append({})
            
    #         # get lineage of each leaf node except for the root
    #         lineage = leaf.lineage[1:]
            
    #         # calculate diff counts between nodes in lineage
    #         cnts = np.array([n.cnt for n in lineage], dtype='float')
    #         diff = np.append((cnts[:-1] - cnts[1:]), cnts[-1])            
    #         btot = sum(diff)
            
    #         # calculate support at each node except the root
    #         for n, node in enumerate(lineage):
    #             attr = node.parent.attr
    #             if attr in support[branch]:
    #                 support[branch][attr] += diff[n] / btot
    #             elif attr != None:
    #                 support[branch][attr] =  diff[n] / btot

    #     print "Calculating support:"
    #     pp.pprint(support)
    #     self.support = support