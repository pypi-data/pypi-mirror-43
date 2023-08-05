import logging
from copy import deepcopy

import pandas as pd

import ssbio.io
import ssbio.utils

log = logging.getLogger(__name__)

class Object(object):
    """Cobra core object with additional methods to update and get attributes"""

    def __init__(self, id=None, description=None, *args, **kwargs):
        self.id = id
        self.description = description
        self.notes = {}

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "<%s %s at 0x%x>" % (self.__class__.__name__, self.id, id(self))

    def update(self, newdata, overwrite=False, only_keys=None):
        """Add/update any attributes from a dictionary.

        Args:
            newdata: Dictionary of attributes
            overwrite: If existing attributes should be overwritten if provided in newdata
            only_keys: List of keys to update

        Examples:
            >>> myobj = Object(id='hi', description='blankname')
            >>> myobj.update({'description':'withname'}, overwrite=False)
            >>> myobj.get_dict() == {'id': 'hi', 'description':'blankname'}
            True

            >>> myobj = Object(id='hi', description='blankname')
            >>> myobj.update({'description':'withname'}, overwrite=True)
            >>> myobj.get_dict() == {'id': 'hi', 'description':'withname'}
            True

            >>> myobj = Object(id='hi', description='blankname')
            >>> myobj.update({'description':'withname', 'randomkey':'randomval'}, overwrite=True)
            >>> myobj.get_dict() == {'id': 'hi', 'description': 'withname', 'randomkey': 'randomval'}
            True

            >>> myobj = Object(id='hi', description='blankname')
            >>> myobj.update({'description':'withname', 'randomkey':'randomval'}, overwrite=True, only_keys='description')
            >>> myobj.get_dict() == {'id': 'hi', 'description': 'withname'}
            True

            >>> myobj = Object(id='hi', description='blankname')
            >>> myobj.update({'description':'withname', 'randomkey':'randomval'}, overwrite=True, only_keys='randomkey')
            >>> myobj.get_dict() == {'id': 'hi', 'description': 'blankname', 'randomkey': 'randomval'}
            True

            >>> myobj = Object(id='hi', description='blankname')
            >>> myobj.update({'description':'withname', 'randomkey':'randomval'}, overwrite=False)
            >>> myobj.get_dict() == {'id': 'hi', 'description': 'blankname', 'randomkey': 'randomval'}
            True

            >>> myobj = Object(id='hi', description='blankname')
            >>> myobj.update({'description':'withname', 'randomkey':'randomval'}, overwrite=False, only_keys='randomkey')
            >>> myobj.get_dict() == {'id': 'hi', 'description': 'blankname', 'randomkey': 'randomval'}
            True

        """
        # Filter for list of keys in only_keys
        if only_keys:
            only_keys = ssbio.utils.force_list(only_keys)
            newdata = {k:v for k,v in newdata.items() if k in only_keys}

        # Update attributes
        for key, value in newdata.items():
            # Overwrite flag overwrites all attributes
            if overwrite:
                setattr(self, key, value)
            else:
                # Otherwise check if attribute is None and set it if so
                if hasattr(self, key):
                    if not getattr(self, key):
                        setattr(self, key, value)
                    else:
                        continue
                # Or just add a new attribute
                else:
                    setattr(self, key, value)

    def get_dict(self, only_attributes=None, exclude_attributes=None, df_format=False):
        """Get a dictionary of this object's attributes. Optional format for storage in a Pandas DataFrame.

        Args:
            only_attributes (str, list): Attributes that should be returned. If not provided, all are returned.
            exclude_attributes (str, list): Attributes that should be excluded.
            df_format (bool): If dictionary values should be formatted for a dataframe
                (everything possible is transformed into strings, int, or float -
                if something can't be transformed it is excluded)

        Returns:
            dict: Dictionary of attributes

        """

        # Choose attributes to return, return everything in the object if a list is not specified
        if not only_attributes:
            keys = list(self.__dict__.keys())
        else:
            keys = ssbio.utils.force_list(only_attributes)

        # Remove keys you don't want returned
        if exclude_attributes:
            exclude_attributes = ssbio.utils.force_list(exclude_attributes)
            for x in exclude_attributes:
                if x in keys:
                    keys.remove(x)

        # Copy attributes into a new dictionary
        df_dict = {}
        for k, orig_v in self.__dict__.items():
            if k in keys:
                v = deepcopy(orig_v)
                if df_format:
                    if v and not isinstance(v, str) and not isinstance(v, int) and not isinstance(v, float) and not isinstance(v, bool):
                        try:
                            df_dict[k] = ssbio.utils.force_string(deepcopy(v))
                        except TypeError:
                            log.warning('{}: excluding attribute from dict, cannot transform into string'.format(k))
                    elif not v and not isinstance(v, int) and not isinstance(v, float):
                        df_dict[k] = None
                    else:
                        df_dict[k] = deepcopy(v)
                else:
                    df_dict[k] = deepcopy(v)
        return df_dict

    def save_dataframes(self, outdir, prefix='df_'):
        """Save all attributes that start with "df" into a specified directory.

        Args:
            outdir (str): Path to output directory
            prefix (str): Prefix that dataframe attributes start with

        """
        # Get list of attributes that start with "df_"
        dfs = list(filter(lambda x: x.startswith(prefix), dir(self)))

        counter = 0
        for df in dfs:
            outpath = ssbio.utils.outfile_maker(inname=df, outext='.csv', outdir=outdir)
            my_df = getattr(self, df)
            if not isinstance(my_df, pd.DataFrame):
                raise TypeError('{}: object is not a Pandas DataFrame'.format(df))

            if my_df.empty:
                log.debug('{}: empty dataframe, not saving'.format(df))
            else:
                my_df.to_csv(outpath)
                log.debug('{}: saved dataframe'.format(outpath))
                counter += 1

        log.debug('Saved {} dataframes at {}'.format(counter, outdir))

    def save_pickle(self, outfile, protocol=2):
        """Save the object as a pickle file

        Args:
            outfile (str): Filename
            protocol (int): Pickle protocol to use. Default is 2 to remain compatible with Python 2

        Returns:
            str: Path to pickle file

        """
        ssbio.io.save_pickle(self, outfile, protocol)

    def __json_encode__(self):
        to_return = {}
        # Don't save properties, methods in the JSON
        for x in [a for a in dir(self) if not a.startswith('__') and not a.startswith('_{}__'.format(type(self).__name__)) and not isinstance(getattr(type(self), a, None), property) and not callable(getattr(self,a))]:
            to_return.update({x: getattr(self, x)})
        return to_return

    def save_json(self, outfile, compression=False):
        """Save the object as a JSON file using json_tricks"""
        ssbio.io.save_json(self, outfile, compression=compression)