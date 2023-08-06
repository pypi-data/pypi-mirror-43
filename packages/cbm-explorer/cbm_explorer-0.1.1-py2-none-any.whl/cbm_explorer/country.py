# Built-in modules #

# Internal modules #
from cbm_explorer import repos_dir

# First party modules #
from autopaths.dir_path   import DirectoryPath
from plumbing.cache       import property_cached
from plumbing.databases.access_database import AccessDatabase

# Third party modules #
import pandas

# Country codes #
all_codes = pandas.read_csv(str(repos_dir + 'data/foastat_countries.csv'))

###############################################################################
class Country(object):
    """This object is represents the data and simulation pertaining to one
    euro country."""

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.country_iso2)

    def __init__(self, data_dir=None):
        """Store the data directory paths where everything will start from."""
        # Main directory #
        self.data_dir = DirectoryPath(data_dir)
        # Check it exists #
        self.data_dir.must_exist()
        # The custom name we find here #
        self.short_name = self.data_dir.name
        # Load name mappings #
        row = all_codes.loc[all_codes['Short name'] == self.short_name].iloc[0]
        # The reference ISO2 code #
        self.country_iso2   = row['ISO2 Code']
        # Store all the country references codes #
        self.country_num    = row['Country Code']
        self.country_name   = row['Country']
        self.country_m49    = row['M49 Code']
        self.country_iso3   = row['ISO3 Code']
        self.nuts_zero_2006 = row['Nuts Zero 2006']
        self.nuts_zero_2016 = row['Nuts Zero 2010']

    @property_cached
    def result_database(self):
        """This is the database that is contained in a directory ending with 'Results'.
        It is named 'Output'."""
        condition = lambda f: f.extension == '.mdb' and f.directory.endswith('Results\\')
        matches = [f for f in self.data_dir.files if condition(f)]
        if len(matches) > 1: raise Exception("Several matches were found for the result database.")
        if len(matches) < 1: raise Exception("No matches were found for the result database.")
        return AccessDatabase(matches[0])

    @property_cached
    def run_database(self):
        """This is the database that is contained in a directory ending with 'Run'.
        It is named 'Input'."""
        condition = lambda f: f.extension == '.mdb' and f.directory.endswith('_run\\')
        matches = [f for f in self.data_dir.files if condition(f)]
        if len(matches) > 1: raise Exception("Several matches were found for the run database.")
        if len(matches) < 1: raise Exception("No matches were found for the run database.")
        return AccessDatabase(matches[0])