import requests
import pandas as pd
from elasticsearch8 import Elasticsearch, NotFoundError
from flask import current_app, request
from dotenv import load_dotenv
import os
load_dotenv()

def main():
    def find_mel_1hr_data(air_data):
        melbourne_cities = [
            'Box Hill', 'Alphington', 'Dandenong', 'Point Cook', 'Melbourne CBD', 
            'Brighton', 'Altona North', 'Healesville', 'Sunbury', 'Macleod', 
            'Spotswood', 'Kingsville', 'Melton', 'Mooroolbark', 'Footscray', 'Brooklyn'
        ]
        
        filtered_df = air_data[air_data['timeSeriesName'] == '1HR_AV']
        mel_df = filtered_df[filtered_df['sit_name'].isin(melbourne_cities)]
        return mel_df

    def preprocess_new_air(df):
        air_data = df
        target_cols = ['sit_name', 'until', 'averageValue']
        air_data2 = air_data.filter(items=target_cols)

        air_data2['until'] = pd.to_datetime(air_data2['until'])
        air_data2['datetime_local'] = air_data2['until'].dt.strftime('%Y-%m-%d-%H')

        air_data2 = air_data2.rename(columns={'sit_name': 'location_name'})
        air_data2 = air_data2.rename(columns={'averageValue': 'BPM2.5'})

        new_order = ['datetime_local', 'location_name', 'BPM2.5']
        air_data2 = air_data2.reindex(columns=new_order)
        air_data2 = air_data2.dropna(subset=['BPM2.5'])

        bpm25_mean = air_data2['BPM2.5'].mean()
        datetime_local = air_data2.iloc[0, 0]

        mel_air = [datetime_local, 'Melbourne', bpm25_mean]
        return mel_air
    def store_data_to_elasticsearch(data):
        es = Elasticsearch(
            hosts=['https://elasticsearch-master.elastic.svc.cluster.local:9200'],
            basic_auth=('elastic', 'elastic'),
            verify_certs=False
        )
        
        bmp2_5 = data[2]
        datetime_local = data[0]
        location_name = data[1]
        document = {
            "BMP2_5": bmp2_5,
            "datetime_local": datetime_local,
            "location_name": location_name
        }
        current_app.logger.info(f'Observations to add:  {document}')

        res = es.index(
            index='aircondition',
            id=f"{datetime_local}",
            body=document
        )
        current_app.logger.info(f'Indexed airconditioni {f"{datetime_local}"}')        
        return 'ok'

    api_key = os.getenv('air_api_key') #"ef4c5176645445238294a9fbf5fa8ad1"
    subscription_name = "comp90024"
    url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air"

    headers = {
        "User-Agent": 'curl/8.4.0',
        "Cache-Control": "no-cache",
        'X-API-Key': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Query failed:", response.status_code)
        return

    def json_to_dataframe(json_data):
        df = pd.json_normalize(json_data['records'])
        return df

    df = json_to_dataframe(data)

    column_0_data = df.iloc[:, 0]
    column_1_data = df.iloc[:, 1]
    column_4_data = df.iloc[:, 4]
    df_main_v2 = pd.DataFrame()

    for i, item in enumerate(column_4_data):
        if isinstance(item, float):
            continue
        if isinstance(item, list):
            for type in item:
                if type["name"] == 'PM2.5':
                    for tsr in type['timeSeriesReadings']:
                        tsr_name = tsr['timeSeriesName']
                        for reading in tsr['readings']:
                            df_temp = pd.DataFrame([reading])
                            df_temp['name'] = 'PM2.5'
                            df_temp['timeSeriesName'] = tsr_name
                            df_temp['sit_id'] = column_0_data[i]
                            df_temp['sit_name'] = column_1_data[i]
                            df_main_v2 = pd.concat([df_main_v2, df_temp])

    df_main_v2 = df_main_v2[['sit_id','sit_name', 'name', 'timeSeriesName', 'since', 'until', 'averageValue', 'unit', 'confidence', 'totalSample', 'healthAdvice', 'healthAdviceColor', 'healthCode']]
    df_main_v2.to_csv("air_data_realtime.csv", index=False)

    realtime_air_1h = find_mel_1hr_data(df_main_v2)
    data = preprocess_new_air(realtime_air_1h)
    
    response = store_data_to_elasticsearch(data)
    return response

if __name__ == '__main__':
    print(main())
