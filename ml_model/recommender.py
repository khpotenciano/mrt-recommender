import pandas as pd
import import_files as MrtRecommendationDependencies
from util import Util
from mrt_ridership_model import MrtRidershipModel
from train_operations_model import TrainOperationsModel
from trip_classifier import TripClassifier
import numpy as np

class Recommender:
    def __init__(self):
        self._ridership_model = MrtRidershipModel()
        self._trains_running_model = TrainOperationsModel()
        self._headway_model = TrainOperationsModel('headway')
        self._weather_df = pd.read_csv(MrtRecommendationDependencies.get_dataset_path("weather_processed.csv"),parse_dates=['datetime'])
        self._classifier = TripClassifier()
        self._stations = ['north','qave','kamuning','cubao','santolan','ortigas','shaw','boni','guada','buendia','ayala','magallanes','taft']

    def predict(self,station,triptime):
        # prev_station = None
        # next_station = None
        # station_index = self._stations.index(station)
        # if station_index < (len(self._stations) - 1):
        #     next_station = self._stations[station_index+1]
        # if station_index > 0:
        #     prev_station = self._stations[station_index-1]
        station_prediction = self.predict_per_station(station,triptime)
        # if prev_station != None:
        #     prev_station_pred = self.predict_per_station(prev_station,triptime)
        # if next_station != None:
        #     next_station_pred = self.predict_per_station(next_station,triptime)
        return station_prediction
        return {
            'station': {'name': station, 'prediction': station_prediction.to_dict(orient='records')}
        }


    def predict_per_station(self,station,triptime):
        station_prediction = self._ridership_model.predict_ridership(station,triptime).rename(columns={'ds': 'datetime', 'entry_pred': 'entry', 'exit_pred':'exit'})
        weather_data = station_prediction.merge(self._weather_df,left_on='datetime', right_on='datetime').fillna(0)
        weather_data['hour_of_day'] = weather_data.apply(lambda x: x.datetime.hour, axis=1)
        weather_data['day_of_week'] = weather_data.apply(lambda x: x.datetime.weekday(), axis=1)
        running_train_prediction = np.round(self._trains_running_model.predict(weather_data))
        weather_data['num_train_running'] = running_train_prediction
        weather_data['num_train_operational'] = running_train_prediction
        headway_pred = np.around(self._headway_model.predict(weather_data),1)
        weather_data['headway'] = headway_pred
        weather_data['recommendation'] = self._classifier.predict(weather_data)
        return weather_data.drop(weather_data.columns.difference(['datetime', 'entry', 'exit', 'num_train_running', 'num_train_operational', 'headway', 'recommendation']), axis=1)
