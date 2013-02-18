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

    def translate(self, value):
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

        print "then branch = %i" % value