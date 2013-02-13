import pandas as pd
import numpy as np
from interaction import Interaction
from io import BytesIO
from lxml import etree
from lxml.etree import tostring
from pandas import Series, DataFrame




# Make some test Data
# TESTING
test = pd.read_csv("breast-cancer-wisconsin.data.txt", header=None, names=['v'+str(i) for i in range(11)])
test['y'] = test['v10'].map({2:0,4:1})
ivs = ['v'+str(i+1) for i in range(9)]
test['v11'] = range(len(test))
ivs.append('v11')

vars = [{'attr':'v1', 'corr':'pos', 'mincnt':50},
        {'attr':'v2', 'corr':'pos', 'mincnt':50},
        {'attr':'v3', 'corr':'pos', 'mincnt':50},
        {'attr':'v4', 'corr':'pos', 'mincnt':50}]

#Stress test
#test = pd.concat([test for i in range(200)], ignore_index=True)



#Logistic test data
##  Attribute                     Domain
#   -- -----------------------------------------
#   1. Sample code number            id number
#   2. Clump Thickness               1 - 10
#   3. Uniformity of Cell Size       1 - 10
#   4. Uniformity of Cell Shape      1 - 10
#   5. Marginal Adhesion             1 - 10
#   6. Single Epithelial Cell Size   1 - 10
#   7. Bare Nuclei                   1 - 10
#   8. Bland Chromatin               1 - 10
#   9. Normal Nucleoli               1 - 10
#  10. Mitoses                       1 - 10
#  11. Class:                        (2 for benign, 4 for malignant)

class DecisionTree():
    #Root node for xml tree representation
    __root = etree.Element("root")

    """Decision tree class"""
    def __init__(self, df, attributes, target):
        self.attributes = attributes
        self.target = target
        self.df = df
    
    #Test program
    def induce(self, df=None, parent=None, side='root'):
        var = raw_input("Press a key to step through")
        if df is None:
            df = self.df

        if parent is None:
            parent = self.__root

        print "Start induce"
        #Find best splits for all attribtues
        attr_splits = self.find_attr_splits(df,
                                            self.attributes, self.target)

        print "Split results:\n", attr_splits

        #Check if a split exists, if so find best and split df
        if ((attr_splits == -1) | (attr_splits == dict())):
            print "Terminating recursion"
            node = etree.Element('leaf', s=side)
            parent.append(node)
            return
        else:
            #Find attribute that best splits the data
            print "Find the best splitting attribute"
            best_attr = self.find_best_attr(attr_splits)
            var = best_attr['name']
            val = best_attr['val']
            iv  = best_attr['iv']
            print "IV = ", iv
            #Create XML content
            node = etree.Element('node', attr=var, val=unicode(val), side=side)
            parent.append(node)

            left, right = self.split_df(df, best_attr)
            print len(left), len(right)
            self.induce(left , parent=node, side='left')
            self.induce(right, parent=node, side='right')


    def find_attr_splits(self, df, dict, y):
        """For list of attributes, find best split for each and return dict
           of results"""
        res = {}
        #For each attribute find the split that maximizes IV
        for d in dict:
            #Unpack the dictionary:
            attr = d['attr']
            corr = d['corr']
            mincnt = d['mincnt']

            print "Getting split for %s" % attr
            try:
                i = Interaction(df[attr], y)
                best_split = i.get_best_split(mincnt=mincnt, corr=corr, verbose=False)
                if best_split == None:
                    print "Split on %s returned None" % attr
                else:
                    res[attr] = best_split
            except TypeError:
                pass
        return res

    def find_best_attr(self, res):
        """Find best splitting attribute from dict of attribute splits"""
        #res = {k:v for k,v in res.items() if v != None}
        attr = max(res, key=lambda x: res[x]['iv'])
        return res[attr]

    def split_df(self, df, tup):
        """Split df on best attr and return left and right dfs"""
        print "Splitting the df"
        attr, val = tup['name'], tup['val']
        print "Attribute: ", attr
        print "Value: ", val
        print "Splitting on %s at value %s" % (attr, val)
        return df[df[attr]<=val], df[df[attr]>val]



#Helper function to calculate IV
# def calc_cuml_IV(cnt):
#     pctsum = cnt.apply(lambda x: x.cumsum()/x.sum().astype(float))
#     cumWoE = pctsum.apply(lambda x: np.log(x[0]/x[1]), axis=1)
#     return cumWoE*(pctsum.ix[:,0] - pctsum.ix[:,1])

# def find_best_split(df, iv, y):
#     """Find value of attribute that best splits the data"""


#     #TODO: add depth constraint
#     #constant mincnt
#     mincnt = 150

#     #check if attribute is an object and not numerical
#     if df[iv].dtype == 'object':
#         return {'splitval':-1, 'split_iv':-1}
    
#     #Create pivot table of attribute crossed with target variable
#     cnt = pd.pivot_table(df[[iv,y]], values=y, rows=iv, cols=y, aggfunc='count')

#     #Cumulative information value ascending
#     iv_asc = calc_cuml_IV(cnt)

#     #Cumulative information values descending
#     iv_dsc = calc_cuml_IV(cnt.sort_index(ascending=False))

#     #Calculate IV at each possible binary split
#     split_iv = (iv_asc + iv_dsc.shift()).fillna(-1)

#     #Minimum leaf count criterion
#     ct_asc = cnt.sum(axis=1).cumsum()
#     ct_dsc = cnt.sort_index(ascending=False).sum(axis=1).cumsum().shift()
#     cnts = ct_asc.align(ct_dsc)
#     cnt_criterion = ((cnts[0]>mincnt)&(cnts[1]>mincnt))

#     #Apply criteria to split_iv array
#     splits = split_iv[cnt_criterion]

#     #Check if splits returns more than 0
#     if (len(splits) == 0):
#         return {'split_val':-1, 'split_iv':-1}
#     else:
#         #Find max values
#         max_split_iv  = splits.max()
#         max_split_val = splits.idxmax()
#         return {'split_val':max_split_val, 'split_iv':max_split_iv}




        

#Create root node
# root = etree.Element("root")

# #Call the tree induction method
# induce(test, root)

# #Store the tree into a string
# s = tostring(root, pretty_print=True)

# #Print the string
# print s


# def translate_tree(root=root):
#     #create iterator of leaf nodes
#     context = etree.iterwalk(root, events=("end",), tag="leaf")

#     #store leaves in array
#     leaves = [elem for action, elem in context]

#     for branch, el in enumerate(leaves):
#         trace(el, branch)

#     return

# def trace(element, branch):
#     sign_dict = dict({'right':'>','left':'<='})
#     el = element.getparent()
#     sign = sign_dict.get(element.get('s'),'root')

#     print "if (%s %s %s) and" % (el.get('attribute'), sign, el.get('value'))
    
#     if (el.get('s') == 'root'):
#         print "tree = %s" % branch
#         return
#     else:
#        trace(el, branch)

# translate_tree()
# #translate tree to SAS code: