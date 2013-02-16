import pandas as pd
import numpy as np
from interaction import Interaction, Split
from io import BytesIO
from lxml import etree
from lxml.etree import tostring
from pandas import Series, DataFrame

class Node(object):
    attr = None
    val  = None
    side = None
    mask = []

    def __init__(self, parent=None, type=None):
        self.parent = parent
        self.type = type

    def get_parent(self):
        return self.parent

    def translate(self):
        s = {'left':'<=', 'right':'>'}
        par = self.get_parent()

        while not par.side == None:
            # node info from parent
            attr, val = (par.attr, par.val)
            if self.type == 'leaf':
                print "I am a leaf"
            else:
                sign = s.get(self.side, 'error')
                print "%s %s %s" % (attr, sign, val)
            return par.translate()


