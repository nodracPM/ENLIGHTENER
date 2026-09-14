import os
import numpy as np
from fca_math.contexts import *
from fca_math.scales import *
from fca_math.fca_utils import *
from fca_math.carrier import *
from fca_math.aldi import *
from fca_math.bonds import *
from fca_math.diagrams import *
from fca_math.implications import *
from fca_math.closures import *
from pathlib import Path
cxtpathname = 'contexts/user/'
predpathname  = 'contexts/predefined/'
bookpathname = 'contexts/gwbook/'
def is_valid_directory(pathname):
    p = Path(pathname)
    return p.exists() and p.is_dir()
if not is_valid_directory(cxtpathname):  os.mkdir(cxtpathname)
if not is_valid_directory(bookpathname): os.mkdir(bookpathname)

