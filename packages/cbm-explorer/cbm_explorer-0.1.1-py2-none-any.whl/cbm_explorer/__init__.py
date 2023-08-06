# Special variables #
__version__ = '0.1.1'

# Built-in modules #
import os, sys

# First party modules #
from autopaths.dir_path import DirectoryPath

# Constants #
project_name = 'cbm_explorer'
project_url  = 'https://webgate.ec.europa.eu/CITnet/stash/projects/BIOECONOMY/repos/cbm_explorer'

# Get paths to module #
self       = sys.modules[__name__]
module_dir = DirectoryPath(os.path.dirname(self.__file__))

# The repository directory #
repos_dir = module_dir.directory

# Path with the data #
countries_dir = os.environ.get('COUNTRIES_DIR', '~/test/')
