#===============================================================================
# jsontab.py
#===============================================================================

"""Agnostically load JSON or tabular data"""




# Imports ======================================================================

import json
import pandas as pd




# Functions ====================================================================

def from_json(
    filepath_or_buffer,
    orient='columns',
    dtype=None,
    columns=None,
    structure='dict',
    **kwargs
):
    """Load a data frame from JSON data

    Parameters
    ----------
    filepath_or_buffer
        file path or buffer providing JSON data
    orient
        passed to pandas.DataFrame.from_dict()
    dtype
        passed to pandas.DataFrame.from_dict()
    columns
        passed to pandas.DataFrame.from_dict()
    kwargs
        other arguments passed to json.load()
    
    Returns
    -------
    DataFrame
        a pandas data frame
    """

    if isinstance(filepath_or_buffer, str):
        with open(filepath_or_buffer, 'r') as f:
            j = json.load(f, **kwargs)
    else:
        j = json.load(filepath_or_buffer, **kwargs)
    if structure == 'dict':
        return {
            k: pd.DataFrame.from_dict(
                v,
                orient=orient,
                dtype=dtype,
                columns=columns
            )
            for k, v in j.items()
        }
    if structure == 'list':
        return [
            pd.DataFrame.from_dict(
                v,
                orient=orient,
                dtype=dtype,
                columns=columns
            )
            for v in j.values()
        ]
    if structure == 'tuple':
        return tuple(
            pd.DataFrame.from_dict(
                v,
                orient=orient,
                dtype=dtype,
                columns=columns
            )
            for v in j.values()
        )


def from_json_or_tab(
    filepath_or_buffer,
    json=False,
    tab=False,
    orient='columns',
    dtype=None,
    columns=None,
    structure='dict',
    **kwargs
):
    """Agnostically load JSON or tabular data

    Parameters
    ----------
    filepath_or_buffer
        a JSON or tabular file or buffer
    json : bool
        if True, expect JSON input
    tab : bool
        if True, expect tabular input
    header : bool
        if True, input file has a header
    kwargs
        other arguments passed to json.load() or pandas.read_csv()
    
    Returns
    -------
    DataFrame
        a pandas data frame
    """

    if json and not tab:
        return from_json(
            filepath_or_buffer,
            orient=orient,
            dtype=dtype,
            columns=columns,
            structure=structure
            **kwargs
        )
    elif tab and not json:
        if structure == 'dict':
            return {0: pd.read_csv(filepath_or_buffer, **kwargs)}
        if structure == 'list':
            return [pd.read_csv(filepath_or_buffer, **kwargs)]
        if structure == 'tuple':
            return (pd.read_csv(filepath_or_buffer, **kwargs),)
    else:
        try:
            return from_json(
                filepath_or_buffer,
                orient=orient,
                dtype=dtype,
                columns=columns,
                structure=structure
                **kwargs
            )
        except:
            if structure == 'dict':
                return {0: pd.read_csv(filepath_or_buffer, **kwargs)}
            if structure == 'list':
                return [pd.read_csv(filepath_or_buffer, **kwargs)]
            if structure == 'tuple':
                return (pd.read_csv(filepath_or_buffer, **kwargs),)
