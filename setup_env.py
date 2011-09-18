
import os
import sys

# putting third party libs in lib directory
lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

# Setting the version of django. Need to import the template
# file before using any django module because that sets up the
# django settings stuff...
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext.webapp import template