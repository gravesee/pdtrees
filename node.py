import pandas as pd
import numpy as np
from interaction import Interaction, Split
from io import BytesIO
from lxml import etree
from lxml.etree import tostring
from pandas import Series, DataFrame

class Node(object):
    attr  = None
    val   = None
    side  = None

    def __init__(self, parent=None, type=None, depth=0):
        self.parent = parent
        self.type = type
        self.depth = depth

    def get_parent(self):
        return self.parent

    def translate(self):
        s = {'left':'<=', 'right':'>'}
        par = self.get_parent()

        if self.type == 'leaf':
            print "\nif"

        # terminate recurions if parent node is root
        while par.attr != None:
            # node info from parent
            attr, val = (par.attr, par.val)
            sign = s.get(self.side, 'error')

            p1 = "%s".ljust(10) % attr
            p2 = "%s".ljust(3)  % sign
            p3 = "%s".rjust(15-len(sign)) % val

            print(p1 + p2 + p3),

            if (self.depth > 1):
                print "and"

            return par.translate()


