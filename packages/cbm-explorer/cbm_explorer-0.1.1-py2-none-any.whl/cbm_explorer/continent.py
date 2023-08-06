# Built-in modules #
from collections import OrderedDict

# Third party modules #
import pandas

# First party modules #
from autopaths.dir_path import DirectoryPath
from plumbing.cache     import property_cached

# Internal modules #
from cbm_explorer.country import Country
from cbm_explorer import countries_dir

###############################################################################
class Continent(object):
    """Aggregates countries together. Enables access to dataframe containing
    concatenates data from all countries."""

    def __getitem__(self, key): return [c for c in self.all_countries if c.country_iso2 == key][0]

    def __iter__(self): return iter(self.all_countries)

    def __init__(self, countries_dir):
        """Store the countries_dir directory path where, inside, there
        is a directory for every country."""
        self.countries_dir = DirectoryPath(countries_dir)

    @property_cached
    def all_countries(self):
        return [Country(d) for d in self.countries_dir.flat_directories]

    @property
    def first(self):
        return self.all_countries[0]

    def grouped_dict(self, name):
        """A dictionary of data frames, with country iso 2 code as keys."""
        dist_all = [(c.country_iso2, c.csv_to_xls.read_csv(name)) for c in self.all_countries]
        return OrderedDict(dist_all)

    def grouped_df(self, name):
        """A concatenated data frame containing disturbance tables for all countries."""
        return pandas.concat(self.grouped_dict(name))

###############################################################################
# Main object #
continent = Continent(countries_dir)



