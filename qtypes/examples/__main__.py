"""Examples runner."""


import sys


from .fs import *
from .units import *


function_name = sys.argv[1]


locals()[function_name]()
