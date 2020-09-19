from datetime import datetime
from fbprophet import Prophet
import pandas as pd
from util import Util

class RidershipModel:

    def __init__(self,field):
        # self._training_data = training_data
        self.init_holidays()
        self._model = Prophet(daily_seasonality=True, weekly_seasonality=True, holidays=self._holidays)
        self._model.add_country_holidays(country_name="PH")
        self._field = field


    def init_holidays(self):
        dates = []
        start = datetime(2019,4,15,0,0)
        end = datetime(2019,4,22,0,0)
        date = start
        while date < end:
            dates.append(date)
            date = Util.get_next_hour(date,1)
        self._holidays = pd.DataFrame({
            'holiday': 'holy week',
            'ds': pd.to_datetime(dates),
            'lower_window': 0,
            'upper_window': 0
        })

    def add_holidays(self,holidays):
        if 'ds' not in holidays.columns:
            holidays['ds'] = ds.index
        self._holidays.append(holidays)

    def fit(self,data):
        self._model.fit(self.prep_data(data))


    def prep_data(self,data,training=True):
        new_df = data.copy()
        if 'ds' not in new_df.columns:
            new_df['ds'] = data.index
        if training:
            new_df['y'] = data[self._field]
        return new_df


    def predict_indiv(self,date):
        predict_df = pd.DataFrame(data=[date], cols=["ds"])
        return self.prep_predict(self._model.predict(predict_df))

    def predict(self,df):
        return self.prep_predict(self._model.predict(self.prep_data(df,False)))

    def predict_steps(self,steps):
        predict_df = self._model.make_future_dataframe(periods=steps,freq='h',include_history=False)
        return self.prep_predict(self._model.predict(predict_df))


    def prep_predict(self, prediction):
        pred_df = prediction.merge(self._holidays, left_on='ds', right_on='ds', how='left').fillna(0)
        pred_df.loc[pred_df['holiday'] != 0, 'prediction'] = 0
        pred_df.loc[pred_df['holiday'] == 0, 'prediction'] = pred_df[pred_df['holiday'] == 0]['yhat']
        return pred_df
