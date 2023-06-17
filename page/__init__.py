
import os
import sys
# print(sys.path)

PAGES_PATH = os.path.normpath(__file__)
sys.path.append(os.path.dirname(PAGES_PATH))

import model
import intro
import generator

