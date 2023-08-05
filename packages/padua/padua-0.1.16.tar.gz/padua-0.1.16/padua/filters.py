import numpy as np
import pandas as pd

def remove_rows_matching(df, column, match):
    """
    Return a ``DataFrame`` with rows where `column` values match `match` are removed.

    The selected `column` series of values from the supplied Pandas ``DataFrame`` is compared
    to `match`, and those rows that match are removed from the DataFrame.

    :param df: Pandas ``DataFrame``
    :param column: Column indexer
    :param match: ``str`` match target
    :return: Pandas ``DataFrame`` filtered
    """
    df = df.copy()
    mask = df[column].values != match
    return df.iloc[mask, :]


def remove_rows_containing(df, column, match):
    """
    Return a ``DataFrame`` with rows where `column` values containing `match` are removed.

    The selected `column` series of values from the supplied Pandas ``DataFrame`` is compared
    to `match`, and those rows that contain it are removed from the DataFrame.

    :param df: Pandas ``DataFrame``
    :param column: Column indexer
    :param match: ``str`` match target
    :return: Pandas ``DataFrame`` filtered
    """
    df = df.copy()
    mask = [match not in str(v) for v in df[column].values]
    return df.iloc[mask, :]

def remove_reverse(df):
    """
    Remove rows with a + in the 'Reverse' column.

    Return a ``DataFrame`` where rows where there is a "+" in the column 'Reverse' are removed.
    Filters data to remove peptides matched as reverse.

    :param df: Pandas ``DataFrame``
    :return: filtered Pandas ``DataFrame``
    """
    return remove_rows_containing(df, 'Reverse', '+')

def remove_contaminants(df):
    """
    Remove rows with a + in the 'Contaminants' column

    Return a ``DataFrame`` where rows where there is a "+" in the column 'Contaminants' are removed.
    Filters data to remove peptides matched as reverse.

    :param df: Pandas ``DataFrame``
    :return: filtered Pandas ``DataFrame``
    """
    colname = (df.columns & ['Contaminant','Potential contaminant'])[0]

    return remove_rows_matching(df, colname, '+')


def remove_only_identified_by_site(df):
    """
    Remove rows with a + in the 'Only identified by site' column

    Return a ``DataFrame`` where rows where there is a "+" in the column 'Only identified by site' are removed.
    Filters data to remove peptides matched as reverse.

    :param df: Pandas ``DataFrame``
    :return: filtered Pandas ``DataFrame``
    """
    return remove_rows_matching(df, 'Only identified by site', '+')


def filter_localization_probability(df, threshold=0.75):
    """
    Remove rows with a localization probability below 0.75

    Return a ``DataFrame`` where the rows with a value < `threshold` (default 0.75) in column 'Localization prob' are removed.
    Filters data to remove poorly localized peptides (non Class-I by default).

    :param df: Pandas ``DataFrame``
    :param threshold: Cut-off below which rows are discarded (default 0.75)
    :return: Pandas ``DataFrame``
    """
    df = df.copy()
    localization_probability_mask = df['Localization prob'].values >= threshold
    return df.iloc[localization_probability_mask, :]


def minimum_valid_values_in_any_group(df, levels=None, n=1, invalid=np.nan):
    """
    Filter ``DataFrame`` by at least n valid values in at least one group.

    Taking a Pandas ``DataFrame`` with a ``MultiIndex`` column index, filters rows to remove
    rows where there are less than `n` valid values per group. Groups are defined by the `levels` parameter indexing
    into the column index. For example, a ``MultiIndex`` with top and second level Group (A,B,C) and Replicate (1,2,3) using
    ``levels=[0,1]`` would filter on `n` valid values per replicate. Alternatively, ``levels=[0]`` would filter on `n`
     valid values at the Group level only, e.g. A, B or C.

    By default valid values are determined by `np.nan`. However, alternatives can be supplied via `invalid`.

    :param df: Pandas ``DataFrame``
    :param levels: ``list`` of ``int`` specifying levels of column ``MultiIndex`` to group by
    :param n: ``int`` minimum number of valid values threshold
    :param invalid: matching invalid value
    :return: filtered Pandas ``DataFrame``
    """
    df = df.copy()
    
    if levels is None:
        if 'Group' in df.columns.names:
            levels = [df.columns.names.index('Group')]

    # Filter by at least 7 (values in class:timepoint) at least in at least one group
    if invalid is np.nan:
        dfx = ~np.isnan(df)
    else:
        dfx = df != invalid
    
    dfc = dfx.astype(int).sum(axis=1, level=levels)
    
    dfm = dfc.max(axis=1) >= n
    
    mask = dfm.values
    
    return df.iloc[mask, :]


def search(df, match, columns=['Proteins','Protein names','Gene names']):
    """
    Search for a given string in a set of columns in a processed ``DataFrame``.

    Returns a filtered ``DataFrame`` where `match` is contained in one of the `columns`.

    :param df: Pandas ``DataFrame``
    :param match: ``str`` to search for in columns
    :param columns: ``list`` of ``str`` to search for match
    :return: filtered Pandas ``DataFrame``
    """
    df = df.copy()
    dft = df.reset_index()
    
    mask = np.zeros((dft.shape[0],), dtype=bool)
    idx = ['Proteins','Protein names','Gene names']
    for i in idx:
        if i in dft.columns:
            mask = mask | np.array([match in str(l) for l in dft[i].values])

    return df.iloc[mask]
    
def filter_exclude(df, s):
    """
    Filter dataframe to exclude matching columns, based on search for "s"
    
    :param s: string to search for, exclude matching columns
    """
    keep = ~np.array( [s in c for c in df.columns.values] )
    return df.iloc[:, keep]

def filter_select_columns_intensity(df, prefix, columns):
    """
    Filter dataframe to include specified columns, retaining any Intensity columns.
    """
    # Note: I use %s.+ (not %s.*) so it forces a match with the prefix string, ONLY if it is followed by something.
    return df.filter(regex='^(%s.+|%s)$' % (prefix, '|'.join(columns)) )

def filter_select_columns_ratio(df, columns):
    """
    Filter dataframe to include specified columns, retaining Ratio columns.
    """
    return df.filter(regex='^(Ratio ./. normalized.*|%s)$' % ('|'.join(columns)) )


def filter_intensity(df, label="", with_multiplicity=False):
    """
    Filter to include only the Intensity values with optional specified label, excluding other 
    Intensity measurements, but retaining all other columns.
    """
    label += ".*__\d" if with_multiplicity else ""

    dft = df.filter(regex="^(?!Intensity).*$")
    dfi = df.filter(regex='^(.*Intensity.*%s.*__\d)$' % label)

    return pd.concat([dft,dfi], axis=1)

def filter_intensity_lfq(df, label="", with_multiplicity=False):
    """
    Filter to include only the Intensity values with optional specified label, excluding other 
    Intensity measurements, but retaining all other columns.
    """
    label += ".*__\d" if with_multiplicity else ""

    dft = df.filter(regex="^(?!LFQ Intensity).*$")
    dfi = df.filter(regex='^(.*LFQ Intensity.*%s.*__\d)$' % label)

    return pd.concat([dft,dfi], axis=1)

def filter_ratio(df, label="", with_multiplicity=False):
    """
    Filter to include only the Ratio values with optional specified label, excluding other
    Intensity measurements, but retaining all other columns.
    """
    label += ".*__\d" if with_multiplicity else ""

    dft = df.filter(regex="^(?!Ratio).*$")
    dfr = df.filter(regex='^(.*Ratio.*%s)$' % label)

    return pd.concat([dft,dfr], axis=1)
