import pandas as pd
import numpy as np
from interaction import Interaction, Split
from io import BytesIO
from lxml import etree
from lxml.etree import tostring
from pandas import Series, DataFrame

class Node(object):
    node_type = 'root'
    split_attr = None
    split_val  = None
    side = None

    def __init__(self, parent, type):
        self.parent = parent
        pass

#I HAVE MADE AN EDIT HERE!!!
#I'm making another edit here!  I'll try to commit