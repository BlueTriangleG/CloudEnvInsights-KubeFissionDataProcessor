import requests
import json
import pandas as pd
import os 

def main():
    # extract mel 1 hour data from real time data
    def find_mel_1hr_data(air_data):
        melbourne_cities = [
            'Box Hill',
            'Alphington',
            'Dandenong',
            'Point Cook',
            'Melbourne CBD',
            'Brighton',
            'Altona North',
            'Healesville',
            'Sunbury',
            'Macleod',
            'Spotswood',
            'Kingsville',
            'Melton',
            'Mooroolbark',
            'Footscray',
            'Brooklyn'
        ]
        
        filtered_df = air_data[air_data['timeSeriesName'] == '1HR_AV']
        mel_df = filtered_df[filtered_df['sit_name'].isin(melbourne_cities)]

        return mel_df

    # preprocess the extracted data
    def preprocess_new_air(df):
        air_data = df

        target_cols = ['sit_name', 'until', 'averageValue']
        air_data2 = air_data.filter(items=target_cols)

        air_data2['until'] = pd.to_datetime(air_data2['until'])
        air_data2['datetime_local'] = air_data2['until'].dt.strftime('%Y-%m-%d-%H')

        # Change col name
        air_data2 = air_data2.rename(columns={'sit_name': 'location_name'})
        air_data2 = air_data2.rename(columns={'averageValue': 'BPM2.5'})

        # change col order
        new_order = ['datetime_local', 'location_name', 'BPM2.5']
        air_data2 = air_data2.reindex(columns=new_order)
        air_data2 = air_data2.dropna(subset=['BPM2.5'])

        bpm25_mean = air_data2['BPM2.5'].mean()
        datetime_local = air_data2.iloc[0, 0]

        mel_air = pd.DataFrame({
            'datetime_local': [datetime_local],
            'location_name': ['Melbourne'],
            'BPM2.5': [bpm25_mean]
        })

        return mel_air
    
    # Extract real time data
    api_key = "ef4c5176645445238294a9fbf5fa8ad1"
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
    
    # Convert JSON data to DataFrame
    def json_to_dataframe(json_data):
        df = pd.json_normalize(json_data['records'])
        return df

    df = json_to_dataframe(data)

    # extract useful information
    column_0_data = df.iloc[:, 0]
    column_1_data = df.iloc[:, 1]
    column_4_data = df.iloc[:, 4]
    df_main_v2 = pd.DataFrame()
    for i, item in enumerate(column_4_data):
        if isinstance(item, float):
            continue  # skip float type data
        
        if isinstance(item, list):
            for type in item:  # loop through each type of monitor data
                if type["name"] == 'PM2.5':
                    for tsr in type['timeSeriesReadings']:  # read data for each time period
                        tsr_name = tsr['timeSeriesName']
                        for reading in tsr['readings']:
                            # create a temporary DataFrame
                            df_temp = pd.DataFrame([reading])
                            # add additional columns
                            df_temp['name'] = 'PM2.5'
                            df_temp['timeSeriesName'] = tsr_name
                            df_temp['sit_id'] = column_0_data[i]
                            df_temp['sit_name'] = column_1_data[i]
                            # concatenate the temporary DataFrame to the main DataFrame
                            df_main_v2 = pd.concat([df_main_v2, df_temp])

    # change column order
    df_main_v2 = df_main_v2[['sit_id','sit_name', 'name', 'timeSeriesName', 'since', 'until', 'averageValue', 'unit', 'confidence', 'totalSample', 'healthAdvice', 'healthAdviceColor', 'healthCode']]

    df_main_v2.to_csv("air_data_realtime.csv", index=False)

    realtime_air_1h = find_mel_1hr_data(df_main_v2)
    realtime_air_df = preprocess_new_air(realtime_air_1h)

    # Convert DataFrame to JSON
    json_result = realtime_air_df.to_json(orient='records')
    json_object = {"data": json.loads(json_result)}
    return json_object
if __name__ == '__main__':
    print(main())
