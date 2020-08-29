import numpy as np
import pandas as pd
import os
from datetime import datetime
import import_files as MrtRecommendationDependencies

class RidershipCleaner:
    station_reference_columns = {
        'north': {'entry': 'North Ave', 'exit': 'Unnamed: 3'},
        'qave': {'entry': 'Quezon Ave', 'exit': 'Unnamed: 5'},
        'kamuning': {'entry': 'GMA Kamuning', 'exit': 'Unnamed: 7'},
        'cubao': {'entry': 'Cubao', 'exit': 'Unnamed: 9'},
        'santolan': {'entry': 'Santolan', 'exit': 'Unnamed: 11'},
        'ortigas': {'entry': 'North Ave', 'exit': 'Unnamed: 13'},
        'shaw': {'entry': 'Shaw Blvd', 'exit': 'Unnamed: 15'},
        'boni': {'entry': 'Boni Ave', 'exit': 'Unnamed: 17'},
        'guada': {'entry': 'Guadalupe', 'exit': 'Unnamed: 19'},
        'buendia': {'entry': 'Buendia', 'exit': 'Unnamed: 21'},
        'ayala': {'entry': 'Ayala Ave', 'exit': 'Unnamed: 23'},
        'magallanes': {'entry': 'Magallanes', 'exit': 'Unnamed: 25'},
        'taft': {'entry': 'Taft', 'exit': 'Unnamed: 27'}
    }
    def __init__(self, doc_path):
        self._doc_path = doc_path
        # self._station = station


    def clean_per_station(self,station,month,include_station=False,save_csv=False):
        path = None
        if "~" in self._doc_path:
            path = os.path.expanduser(self._doc_path)
        else:
            path = os.path.abspath(self._doc_path)
        df = pd.read_excel(open(path, "rb"),sheet_name=month.upper())
        temp_df = pd.DataFrame()
        temp_df['date'] = df['DATE']
        temp_df['time'] = df['TIME']
        if include_station:
            temp_df['station'] = station
        temp_df['entry'] = df[RidershipCleaner.station_reference_columns[station]['entry']]
        temp_df['exit'] = df[RidershipCleaner.station_reference_columns[station]['exit']]
        cleaned_df = temp_df[temp_df.apply(lambda x: not pd.isnull(x.date),axis=1)]
        cleaned_df.fillna(value=0,inplace=True)

        if save_csv:
            filename = f"{station}_{month}.csv"
            self.save_csv(filename,cleaned_df)
        return cleaned_df


    def clean_all(self,month,save_csv=False):
        dfs = []
        for station in RidershipCleaner.station_reference_columns.keys():
            dfs.append(self.clean_per_station(station,month.upper(),True))

        final_dataframe = pd.concat(dfs)
        if save_csv:
            filename = f"{month}.csv"
            self.save_csv(filename,final_dataframe)
        return final_dataframe

    def clean_months(self,station,months=[],save_csv=False):
        dfs = []
        for month in months:
            dfs.append(self.clean_per_station(station,month.upper(),False))
        final_dataframe = pd.concat(dfs)
        if save_csv:
            filename = f"{station}.csv"
            self.save_csv(filename,final_dataframe)
        return final_dataframe

    def save_csv(self,filename,df):
        filepath = os.path.join(MrtRecommendationDependencies.DATASET_PATH, filename)
        df.to_csv(filepath, index=False)
        print(f"Dataframe saved to {filepath}")
