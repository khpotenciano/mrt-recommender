import numpy as np
import pandas as pd
from datetime import datetime
from util import Util
import import_files as MrtRecommendationDependencies
import os

class RidershipTransformer:

    def __init__(self,df):
        self._df = df

    def transform(self,save_csv=False,filename="transformed_dataset"):
        transformed_df = pd.DataFrame()
        transformed_df['datetime'] = self._df.apply(lambda x: datetime.combine(x.date, Util.string_to_time(x.time[0:5])), axis=1)
        transformed_df['entry'] = self._df['entry']
        transformed_df['exit'] = self._df['exit']
        if save_csv:
            self.save_csv(filename, transformed_df)
        return transformed_df

    def save_csv(self,filename,df):
        filepath = os.path.join(MrtRecommendationDependencies.DATASET_PATH, filename)
        df.to_csv(filepath, index=False)
        print(f"Dataframe saved to {filepath}")
