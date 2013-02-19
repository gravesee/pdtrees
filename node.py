import numpy as np
# TODO: Done -- separate printing and lineage functions

class Node(object):
    def __init__(self, parent=None, type=None, depth=0, cnt=0):
        self.parent = parent
        self.type   = type
        self.depth  = depth
        self.attr   = None
        self.val    = None
        self.side   = None
        self.cnt    = cnt
        self.lineage = [self]
        self.get_lineage()

    def get_parent(self):
        return self.parent

    def get_lineage(self):
        """get all ancestors of node including self and return list.
           Reverse the list so order is root --> self"""
        if self.parent == None:
            return
        parent = self.parent
        while parent.attr != None:
            self.lineage.append(parent)
            parent = parent.parent
        self.lineage.reverse()

    def get_branch(self, maxdepth):
        """Calculate branch number based on left, right splits"""
        val = {'left':0, 'right':1}
        tmp = [n for n in range(maxdepth)]
        tmp.reverse()
        divs = [2**i for i in tmp]

        lineage = self.lineage[1:]
        splits = [val[node.side] for n, node in enumerate(lineage)]

        tpl = zip(divs, splits)
        branch = sum([reduce(lambda x,y: x*y, tp) for tp in tpl])
        return branch

    def calc_support(self):
        support = {}
            
        # get lineage of each leaf node except for the root
        lineage = self.lineage[1:]
        
        # calculate diff counts between nodes in lineage
        cnts = np.array([n.cnt for n in lineage], dtype='float')
        diff = np.append((cnts[:-1] - cnts[1:]), cnts[-1])
        btot = sum(diff)
        
        # calculate support at each node except the root
        for n, node in enumerate(lineage):
            attr = node.parent.attr
            if attr in support:
                support[attr] += diff[n] / btot
            elif attr != None:
                support[attr] =  diff[n] / btot

        return support

    def print_node(self):
        """print node in SAS formatting style"""
        s = {'left':'<=', 'right':'>'}
        if self.side == 'root':
            return "if "

        attr = self.parent.attr
        val  = self.parent.val
        sign = s.get(self.side, 'error')
        
        p1 = "%s".ljust(10) % attr
        p2 = "%s".ljust(3)  % sign
        p3 = "%s".rjust(15-len(sign)) % val
        # p4 = "  Support: %.3f" % self.support

        return (p1 + p2 + p3)

    def translate(self, branch):
        """print entire rule in SAS formatting style"""
        num_ancestors = len(self.lineage)

        for n, ancestor in enumerate(self.lineage):
            text = ancestor.print_node()
            if n == 0:
                print(text),
            elif n == 1:
                print text               
            elif n < num_ancestors:
                print "and "+text
            else:
                print "   "+text

        print "then branch = %s" % branch