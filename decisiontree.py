import pandas as pd
import numpy as np
from interaction import Interaction, Split
from lxml import etree
from lxml.etree import tostring
from pandas import Series, DataFrame
from node import Node

class DecisionTree(object):
    """Decision tree class"""

    def __init__(self, df, attributes, target):
        self.df = df
        self.attributes = attributes
        self.target = target
        self.__root = Node(type='root')
        self.__leaves = []
    
    #Test program
    def induce(self, df=None, parent=None, side='root', depth=0):
        # var = raw_input("Press a key to step through")
        if df is None:
            df = self.df

        if parent is None:
            parent = self.__root

        print "Start induce"
        #Find best splits for all attribtues
        splits = self.get_splits(df, self.attributes, self.target)

        #Check if a split exists, if so find best and split df
        found_split = np.any([s.has_split() for s in splits])
        if ((not found_split) | (depth >= 5)):
            print "Terminating recursion"
            node = Node(parent, type='leaf', depth=depth)
            node.side = side
            self.__leaves.append(node)
            return
        else:            
            #Find attribute that best splits the data
            best_attr = self.get_max_split(splits)
            attr, val, pos, iv = best_attr.get_split()

            node = Node(parent, type='node', depth=depth)
            node.attr, node.val, node.side = (attr, val, side)

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
        for n, leaf in enumerate(self.__leaves):
            leaf.translate()
            print "\nthen tree = %s" % n