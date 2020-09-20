import import_files as MrtRecommendationDependencies
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pickle5 as pickle

class TripClassifier:

    def __init__(self, build_from_scratch=False):

        if build_from_scratch or not MrtRecommendationDependencies.model_exists("trip_classifier.sav"):
            self.init_model()
            X, Y = self.init_training_data()
            self.train_model(X,Y)
        else:
            self._model = pickle.load(open(MrtRecommendationDependencies.get_model_path("trip_classifier.sav"), "rb"))

    def dump_model(self):
        pickle.dump(self._model, open(MrtRecommendationDependencies.get_model_path("trip_classifier.sav"), "wb"))


    def init_model(self):
        self._model = Pipeline([('scaler', StandardScaler()), ('pca', PCA(n_components=0.99)), ('classifier', RandomForestClassifier(n_estimators=56, random_state=3))])

    def init_training_data(self):
        df = pd.read_csv(MrtRecommendationDependencies.get_dataset_path("trip_classes.csv"))
        return self.prep_data(df)

    def prep_data(self, data, training=True):
        if training:
            return data.drop(['recommendation', 'hour_of_day', 'day_of_week'], axis=1), data['recommendation']
        else:
            return data.drop(data.columns.difference(['entry', 'exit', 'num_train_running', 'num_train_operational', 'headway', 'temp', 'humidity','rain_1h', 'rain_3h']), axis=1)

    def train_model(self,X,Y):
        self._model.fit(X,Y)

    def predict(self, data):
        return self._model.predict(self.prep_data(data, False))
