# -*- coding: utf-8 -*-
# Namespace dance baby
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

import sys
import os
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

print '*' * 100
print sys.path


