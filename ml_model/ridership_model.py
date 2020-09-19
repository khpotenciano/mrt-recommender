from datetime import datetime
from fbprophet import Prophet
import pandas as pd

class RidershipTransformer:

    def __init__(field):
        # self._training_data = training_data
        self._model = Prophet(daily_seasonality=True, weekly_seasonality=True)
        self._model.add_country_holidays(country_name="PH")
        self._field = field


    def fit(data):
        self._model.fit(self.prep_data(train_set))


    def prep_data(data,training=True):
        new_df = data.copy()
        if 'ds' not in new_df.columns:
            new_df['ds'] = data.index
        if training:
            new_df['y'] = data[self._field]
        return new_df


    def predict_indiv(date):
        predict_df = pd.DataFrame(data=[date], cols=["ds"])
        return self._model.predict(predict_df)

    def predict(df):
        return self._model.predict(self.prep_data(df,False))

    def predict_steps(steps):
        predict_df = self._model.make_future_dataframe(periods=steps,freq='h',include_history=False)
        return self._model.predict(predict_df)
