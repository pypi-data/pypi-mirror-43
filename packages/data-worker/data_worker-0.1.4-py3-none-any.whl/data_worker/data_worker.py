from data_worker.defined_wrappers import wrappers
from data_worker import mapper
from data_worker import utils

import pandas as pd
import json
import os

DATA_WORKER_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'


class DataWorker:

    def __init__(self, sources=None):
        if sources is None:
            sources = wrappers.keys()
        elif not isinstance(sources, list):
            sources = [sources]
        self.wrappers = [mapper.get_wrapper(source) for source in sources]

    def get(self, source, dataset, **kwargs):
        wrapper = mapper.get_wrapper(source)
        wrapper_method = mapper.get_wrapper_method(wrapper, dataset)
        df = wrapper_method(**kwargs)
        self._format(df)
        return df

    def _format(self, df):
        df.rename(utils.column_rename, axis=1, inplace=True)
        df.columns = [col.lower() for col in df.columns]
        if 'timestamp' in df:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
