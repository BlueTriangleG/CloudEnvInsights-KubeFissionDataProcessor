import requests
import json
import pandas as pd


# Extract real time data
api_key = "ef4c5176645445238294a9fbf5fa8ad1"
subscription_name = "comp90024"
url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air"

headers = {
    "User-Agent": 'curl/8.4.0',
    "Cache-Contrl": "no-cache",
    'X-API-Key': api_key
}


response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
        
else:
    print("query fail:", response.status_code)







file_path = "real_time_data.json"

# record data
with open(file_path, "w") as json_file:
    json.dump(response.json(), json_file)


def json_to_dataframe(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # 将JSON数组转换为DataFrame
    df = pd.json_normalize(data['records'])

    
    return df


df= json_to_dataframe(file_path)

# 提取有用的信息
column_0_data = df.iloc[:, 0]
column_1_data = df.iloc[:, 1]
column_4_data = df.iloc[:, 4]
df_main_v2 = pd.DataFrame()
for i, item in enumerate(column_4_data):
    if isinstance(item, float):
        
        continue  # 跳过 float 类型的数据
    
    if isinstance(item, list) :
        for type in item: #循环每种监控器类型读到的数据
            if type["name"] ==  'PM2.5':
                for tsr in type['timeSeriesReadings']: # 读取每种时间段的数据
                    tsr_name = tsr['timeSeriesName']
                    # 遍历 readings
                    for reading in tsr['readings']:
                        # 将每个 reading 转换为 DataFrame
                        df_temp = pd.DataFrame([reading])
                        # 添加 name 和 timeSeriesName 列
                        df_temp['name'] = 'PM2.5'
                        df_temp['timeSeriesName'] = tsr_name
                        df_temp['sit_id'] = column_0_data[i]
                        df_temp['sit_name'] = column_1_data[i]
                        # 将结果添加到主 DataFrame
                        df_main_v2 = pd.concat([df_main_v2, df_temp])

# 重新排序列
df_main_v2 = df_main_v2[['sit_id','sit_name', 'name', 'timeSeriesName', 'since', 'until', 'averageValue', 'unit', 'confidence', 'totalSample', 'healthAdvice', 'healthAdviceColor', 'healthCode']]

df_main_v2.to_csv("air_data_realtime.csv", index=False)