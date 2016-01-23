import pandas as pd

from collections import defaultdict
from sqlalchemy.inspection import inspect

def _query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

def query_to_df(rset):
    return pd.DataFrame(_query_to_dict(rset))
