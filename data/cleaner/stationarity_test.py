from statsmodels.tsa.stattools import adfuller, kpss
import pandas as pd
class StationarityTest:
    @classmethod
    def perform_adfuller(cls, df,*,lag=None):
        dftest = adfuller(df, autolag='AIC',maxlag=lag)
        dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
        for key,value in dftest[4].items():
           dfoutput['Critical Value (%s)'%key] = value
        print (dfoutput)

    @classmethod
    def perform_kpss(cls,df,*,lag=None,regression='ct'):
        kpsst = kpss(df)
        kpsstest = kpss(df, regression=regression,nlags=lag)
        kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
        for key,value in kpsstest[3].items():
            kpss_output['Critical Value (%s)'%key] = value
        print(kpss_output)
