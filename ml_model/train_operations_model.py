import import_files as MrtRecommendationDependencies
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer
import pickle5 as pickle

class TrainOperationsModel:

    def __init__(self,field='num_train_running',build_from_scratch=False):
        self._field = field
        if build_from_scratch or not MrtRecommendationDependencies.model_exists(f"{field}_model.sav"):
            self.init_training_data()
            self.init_model()
            self.train_model()
        else:
            self._model = pickle.load(open(MrtRecommendationDependencies.get_model_path(f"{self._field}_model.sav"), "rb"))

    def dump_model(self):
        pickle.dump(self._models, open(MrtRecommendationDependencies.get_model_path(f"{self._field}_model.sav"), "wb"))

    def init_training_data(self):

        self._train_df = pd.read_csv(MrtRecommendationDependencies.get_dataset_path("train_updates_with_ridership.csv"))
        self._train_x = self.prep_data(self._train_df)
        self._train_y = self._train_df[self._field]

    def init_model(self):
        estimator_count = {
            'num_train_running':52,
            'headway':59
        }
        self._model = Pipeline([('scaler', Normalizer()),('regressor', RandomForestRegressor(n_estimators=estimator_count[self._field],random_state=35))])

    def train_model(self):
        self._model.fit(self._train_x, self._train_y)

    def prep_data(self,data,training=True):
        fields_to_drop = []
        if training:
            fields_to_drop = ['num_dalian_train_running', 'num_dalian_train_operational', 'headway']
            if self._field == "num_train_running":
                fields_to_drop.append('num_train_operational')
                fields_to_drop.append('num_train_running')
        else:
            fields_to_drop.append('weather_main')
            fields_to_drop.append('datetime')

        return data.drop(fields_to_drop, axis=1)

    def predict(self,df):
        return self._model.predict(self.prep_data(df,False))
