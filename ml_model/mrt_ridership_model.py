from ridership_model import RidershipModel
import pandas as pd
import import_files as MrtRecommendationDependencies
from util import Util
import pickle5 as pickle
import numpy as np

class MrtRidershipModel:

    def __init__(self,build_from_scratch=False):
        if build_from_scratch or not MrtRecommendationDependencies.model_exists("ridership_model.sav"):
            self.build_models()
        else:
            self._models = pickle.load(open(MrtRecommendationDependencies.get_model_path("ridership_model.sav"), "rb"))


    def dump_model(self):
        pickle.dump(self._models, open(MrtRecommendationDependencies.get_model_path("ridership_model.sav"), "wb"))

    def build_models(self):
        self._stations = ['north','qave','kamuning','cubao','santolan','ortigas','shaw','boni','guada','buendia','ayala','magallanes','taft']
        self.init_models()
        self.train_models()
    def init_models(self):
        self._models = {}
        for station in self._stations:
            self._models[station] = {'entry': RidershipModel('entry'), 'exit': RidershipModel('exit')}

    def train_models(self):
        for station in self._stations:
            training_data = pd.read_csv(MrtRecommendationDependencies.get_dataset_path(f"{station}_weather_transformed.csv"), parse_dates=["datetime"], index_col="datetime")
            self._models[station]['entry'].fit(training_data)
            self._models[station]['exit'].fit(training_data)

    def predict_ridership(self, station,trip_time):
        hour_prior = Util.get_next_hour(trip_time, -1)
        hour_after = Util.get_next_hour(trip_time, 1)
        df = pd.DataFrame(data=[hour_prior,trip_time,hour_after],columns=["ds"])
        entry_pred = np.round(self._models[station]['entry'].predict(df))
        exit_pred = np.round(self._models[station]['exit'].predict(df))
        return_df = pd.DataFrame()
        return_df['ds'] = df['ds']
        return_df['entry_pred'] = entry_pred['prediction']
        return_df['exit_pred'] = exit_pred['prediction']
        return return_df
