import numpy as np
import pandas as pd
from datetime import datetime
from util import Util
import import_files as MrtRecommendationDependencies

class RidershipTransformer:

    def __init__(self,df):
        self._df = df

    def transform(self,save_csv=False):
        transformed_df = pd.DataFrame()
        transformed_df['datetime'] = self._df.apply(lambda x: datetime.combine(x.date, Util.string_to_time(x.time[0:5])), axis=1)
        transformed_df['entry'] = self._df['entry']
        transformed_df['exit'] = self._df['exit']
        return transformed_df
