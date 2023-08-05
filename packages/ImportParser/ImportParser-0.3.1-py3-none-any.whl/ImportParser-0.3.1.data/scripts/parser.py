#!python

import sys
import os

os.system("pylint " + sys.argv[1] + " --load-plugins=" + sys.argv[2])
