import json
import requests
import pandas as pd
from elasticsearch8 import Elasticsearch
from flask import current_app, request


def main():
    def clean_weather_data(df, location_name):
        columns_drop = ['weather', 'swell_height', 'sea_state', 'swell_period', 'press_tend',
                        'swell_dir_worded', 'wmo', 'history_product', 'cloud_base_m', 'cloud_oktas', 
                        'cloud', 'cloud_type_id', 'cloud_type', 'aifstime_utc', 'local_date_time', 
                        'sort_order', 'vis_km', 'rain_trace']
        df_cleaned = df.drop(columns=columns_drop)
        df_cleaned['name'] = location_name

        df_cleaned['local_date_time_full'] = pd.to_datetime(df_cleaned['local_date_time_full'], format='%Y%m%d%H%M%S')
        df_cleaned['local_date_time_full'] = df_cleaned['local_date_time_full'].dt.strftime('%Y-%m-%d-%H')

        if len(df_cleaned) > 1 and df_cleaned.iloc[0]['local_date_time_full'] != df_cleaned.iloc[1]['local_date_time_full']:
            df_cleaned = df_cleaned.drop(0)
        
        return df_cleaned

    def bom_first_two(realtime_df, location_name):
        first_two_rows = realtime_df.head(3)
        df = clean_weather_data(first_two_rows, location_name)
        return df

    def combine_1h(df):
        mask = df['local_date_time_full'].shift(-1) == df['local_date_time_full']
        rows_to_append = []
        
        for idx in range(0, len(df) - 1, 2):
            if df.iloc[idx]['local_date_time_full'] == df.iloc[idx + 1]['local_date_time_full']:
                combined_row = df.iloc[idx].copy()
                for col in df.columns:
                    if col not in ['sort_order', 'local_date_time_full', 'name']:
                        if isinstance(combined_row[col], list):
                            combined_row[col].append(df.iloc[idx + 1][col])
                        elif isinstance(combined_row[col], str):
                            combined_row[col] = [combined_row[col], df.iloc[idx + 1][col]]
                        else:
                            combined_row[col] = (combined_row[col] + df.iloc[idx + 1][col]) / 2
                rows_to_append.append(combined_row)

        processed_df = pd.DataFrame(rows_to_append, columns=df.columns)
        return processed_df
    
    def store_data_to_elasticsearch(data):
        document = json.dumps(data, indent=4)
        print(document)
        es = Elasticsearch(
            hosts=['https://elasticsearch-master.elastic.svc.cluster.local:9200'],
            basic_auth=('elastic', 'elastic'),
            verify_certs=False
        )
        doc_id = f"{data['local_date_time_full']}-{data['name']}"
        current_app.logger.info(f'add:  {document}')

        res = es.index(
            index='weathercondition',
            id= doc_id,
            body = document
        )
        current_app.logger.info(f'Indexed observation {doc_id}')
        return 'ok'
    
    bom_data_mel = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()['observations']['data']

    df_mel = pd.DataFrame(bom_data_mel)

    cleaned_mel = bom_first_two(df_mel, 'Melbourne CBD')

    combined_mel = combine_1h(cleaned_mel)
    records = combined_mel.to_dict(orient='records')[0]
    response = store_data_to_elasticsearch(records)
    
    return response
