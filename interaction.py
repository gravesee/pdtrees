import pandas as pd
import numpy as np
from pandas import Series, DataFrame

# Interaction class
# Class describing relationship between independent and dependet variable
class Split(object):
    """Class to hold information about a split"""
    val  = None
    pos  = None
    iv   = None
    def __init__(self, name):    
        self.name = name

    def has_split(self):
        return True if self.val is not None else False

    def get_split(self):
        return (self.name, self.val, self.pos, self.iv)


class Interaction(object):
    """
    Object describing the relationship between an independent and Dependent
    variable.  

    Parameters
    ----------
    x : Independent variable of type Series and dtype numeric
    y : Dependent target variable {0,1}
    """
    def __init__(self, x, y):
        #Check that y is set([0,1])
        if not (set(y) == set([0,1])):
            print "y var is not a numeric, 0/1 variable!"
            #TODO: raise exception

        #Check that x is numeric
        if (x.dtype == 'object'):
            raise TypeError("x must be numeric, not object")
            #TODO: raise exception

        #TODO: check that x and y are the same length

        self.x = x
        self.y = y

        #DataFrame of var x and response y
        df = pd.DataFrame({x.name:x, y.name:y})
        self.df = self.__agg(df)

        #Check that x has more than 1 value
        if (len(self.df.index) <= 1):
            raise TypeError("X has <= 1 levels")

        stats = self.__generate_stats(self.df)
        self.split_iv  = stats[0]
        self.split_ct  = stats[1]
        self.split_woe = stats[2]
        self.tot_iv    = stats[3]

    def __agg(self, df):
        """Groupby unique values of IV and get 0,1 counts"""
        grp = df.groupby(self.x.name)[self.y.name]
        df = grp.agg({0: lambda x: (x==0).sum(),
                      1: lambda x: (x==1).sum()})

        #Need consecutive index so store orignal and reset
        self.original_index = df.index
        #Not sure if I need to do this step anymore...
        df.reset_index(inplace=True, drop=True)
        df =  self.__collapse(df)
        
        return df

    def __generate_stats(self, df):
        """Calculate ascending, descending metrics for each possible split"""
        asc_tot = df.sum(axis=1).cumsum()
        dsc_tot = asc_tot.max() - asc_tot

        asc_woe, asc_iv = self.__cum_iv(df)
        dsc_woe, dsc_iv = self.__cum_iv(df.sort_index(ascending=False).shift())

        #Create ascending, descending values for each possible split
        split_iv  = DataFrame(zip(*asc_iv.align(dsc_iv)))
        split_ct  = DataFrame(zip(*asc_tot.align(dsc_tot)))
        split_woe = DataFrame(zip(*asc_woe.align(dsc_woe)))

        #Calculate total iv for interaction
        tot_iv = self.__calc_iv(df)

        return (split_iv, split_ct, split_woe, tot_iv)

    def split(self, mincnt=100, corr='none', verbose=False):
        #Create Split instance to store and pass split info
        split = Split(self.x.name)
        
        #Specify minimum counts required for each child node
        adequate_cts = ((self.split_ct[0]>=mincnt) & 
                        (self.split_ct[1]>=mincnt))

        #Optionally pass relationship between x and y
        if corr == 'neg':
            correlation = ((self.split_woe[0] <  self.split_woe[1]))
        elif corr == 'pos':
            correlation = ((self.split_woe[0] >= self.split_woe[1]))
        else:
            correlation = True

        #Filter out infinite values
        not_inf = (self.split_iv != np.inf).all(axis=1)
        
        candidates = self.split_iv.sum(axis=1).ix[adequate_cts & correlation & not_inf]

        if verbose==True:
            self.print_summary()
        
        #Check if there are any candidates
        if len(candidates) > 0:
            #store split information in Split instance
            split_pos = candidates.idxmax()
            split_val = self.original_index[split_pos]

            split.val  = split_val
            split.pos  = split_pos
            split.iv   = candidates[split_pos]

        return split

    def __collapse(self, df):
        """Collapse rows with zero entries"""
        #Check if all entries are zero
        if np.alltrue((df == 0).any(1)):
            print "All rows have a zero"
            #TODO: Add exception
            raise TypeError("Pity da foo")
            return
        #Find zero rows
        zeros = (df == 0).any(axis=1)
        
        #Group non-zero rows with adjacent zero rows
        grpby = (zeros == False).astype(int).cumsum() - 1
        df = df.groupby(grpby).sum()
        
        df.index = grpby.drop_duplicates().index
        return df

    def print_summary(self):
        print '\n','#'*20, 'Interaction Summary', '#'*20, '\n'
        print 'Independent Variable ..... %s' % self.x.name
        print 'Dependent Variable ....... %s' % self.y.name
        print 'Interaction IV ........... %.2f' % self.tot_iv

        self.print_list(self.split_woe, "WoE")
        self.print_list(self.split_ct , "Counts")
        self.print_list(self.split_iv , "Split IV")
        
        return

    def print_list(self,list,title):
        print "\n%s" % title
        print "---------------------------"
        print "| Val  |  Upper  |  Lower |"
        print "---------------------------"
        for n, row in list.iterrows():
            print "  %s    |  %.2f   |  %.2f" % (self.original_index[n], row[0], row[1])
        return

    def __cum_iv(self, df):
        """Calculate cumulative WoE and IV for interaction"""
        pct_sum = df.apply(lambda x: x.cumsum()/x.sum().astype(float))
        cum_woe = pct_sum.apply(lambda x: np.log(x[0]/x[1]), axis=1)
        cum_iv  = cum_woe*(pct_sum[0] - pct_sum[1])
        return cum_woe, cum_iv

    def __calc_iv(self, df):
        """Calculate information value of the overall interaction"""
        colpct = df/df.sum()
        woe = colpct.apply(lambda x: np.log(x[0]/x[1]), axis=1)
        iv  = (woe*(colpct[0] - colpct[1])).sum()
        return iv

# TESTING
test = pd.read_csv("breast-cancer-wisconsin.data.txt", header=None, names=['v'+str(i) for i in range(11)])
test['y'] = test['v10'].map({2:0,4:1})
ivs = ['v'+str(i+1) for i in range(9)]
test['v11'] = range(len(test))