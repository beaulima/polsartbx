"""Top-level package for the 'pyatcortbx' framework.
Running ``import pyatcortbx`` will recursively import all important subpackages and modules.
"""

import logging

import polsartbx.cli
import polsartbx.utils
import polsartbx.apps
import polsartbx.data
import polsartbx.models
import polsartbx.optims
import polsartbx.transforms
import polsartbx.utils
import polsartbx.polsarproc
import polsartbx.test

logger = logging.getLogger("pyatcortbx")

__url__ = "https://github.com/beaulima/polsartbx"
__version__ = "0.1.0-dev"