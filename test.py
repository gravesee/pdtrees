from decisiontree import DecisionTree
import pandas as pd


#TODO LIST:

# Done -- Add support information to node class
# Abstract the splitting criteria in Interaction class
#    pass a function(s) to Interaction.split instead of hard-coded to IV
# Add support for discrete attributes
# Add ability to pass a binning function in the attribute definition
# Understand and add proper exception handling
# Add some sort of configuration object
# Add formatted printing and logging


# script for testing pdtrees

# Make some test Data
test = pd.read_csv("breast-cancer-wisconsin.data.txt", header=None, names=['v'+str(i) for i in range(11)])
# Stress test
test = pd.concat([test for i in range(20)], ignore_index=True)
test['y'] = test['v10'].map({2:0,4:1})
ivs = ['v'+str(i+1) for i in range(9)]
test['v11'] = range(len(test))
ivs.append('v11')

vars = [{'attr':'v1', 'corr':'pos', 'mincnt':25},
        {'attr':'v2', 'corr':'pos', 'mincnt':25},
        {'attr':'v3', 'corr':'pos', 'mincnt':25},
        {'attr':'v4', 'corr':'pos', 'mincnt':25},
        {'attr':'v5', 'corr':'pos', 'mincnt':25},
        {'attr':'v7', 'corr':'pos', 'mincnt':25},
        {'attr':'v8', 'corr':'pos', 'mincnt':25},
        {'attr':'v9', 'corr':'pos', 'mincnt':25}]

d = DecisionTree(test, vars, 'y')
d.maxdepth = 3
d.build_tree()
# s = d.calc_support()
d.print_tree()
# l = d.leaves
# for leaf in l:
#     leaf.translate()



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