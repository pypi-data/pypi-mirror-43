# Built-in modules #

# Internal modules #
from cbm_explorer import countries_dir

# First party modules #
from plumbing.databases.access_database import AccessDatabase

# Third party modules #

###############################################################################
class VolincDatabase(AccessDatabase):
    pass

###############################################################################
volinc = VolincDatabase(countries_dir + 'VOLINC_Summary.mdb')