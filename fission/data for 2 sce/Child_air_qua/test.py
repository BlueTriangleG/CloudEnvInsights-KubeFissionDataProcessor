
# import requests
# import json
# import pandas as pd

# def main():
#     # 提取实时数据
#     api_key = "ef4c5176645445238294a9fbf5fa8ad1"
#     subscription_name = "comp90024"
#     url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air"

#     headers = {
#         "User-Agent": 'curl/8.4.0',
#         "Cache-Control": "no-cache",
#         'X-API-Key': api_key
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#     else:
#         print("Query failed:", response.status_code)
#         return None

#     file_path = "real_time_data.json"

#     # 记录数据
#     with open(file_path, "w") as json_file:
#         json.dump(response.json(), json_file)

#     def json_to_dataframe(file_path):
#         with open(file_path, 'r') as file:
#             data = json.load(file)
#         # 将 JSON 数组转换为 DataFrame
#         df = pd.json_normalize(data['records'])
#         return df
    
#     # 调用函数以为df赋值
#     df = json_to_dataframe(file_path)
    
#     # 打印 DataFrame
#     print(df)

#     # 提取有用的信息
#     column_1_data = df.iloc[:, 1]
#     column_4_data = df.iloc[:, 4]
#     column_6_data = df.iloc[:, 6]
#     df_main_v2 = pd.DataFrame()
#     for i, item in enumerate(column_4_data):
#         if isinstance(item, float):
#             continue  # 跳过 float 类型的数据
        
#         if isinstance(item, list):
#             for type in item: # 循环每种监控器类型读到的数据
#                 if type["name"] == 'PM2.5':
#                     for tsr in type['timeSeriesReadings']: # 读取每种时间段的数据
#                         tsr_name = tsr['timeSeriesName']
#                         # 遍历 readings
#                         for reading in tsr['readings']:
#                             # 将每个 reading 转换为 DataFrame
#                             df_temp = pd.DataFrame([reading])
#                             # 添加 name 和 timeSeriesName 列
#                             df_temp['location_name'] = column_1_data[i]
#                             # 添加经度和纬度
#                             if len(column_6_data[i]) >= 2:
#                                 df_temp['latitude'] = column_6_data[i][0]
#                                 df_temp['longitude'] = column_6_data[i][1]
#                             else:
#                                 df_temp['latitude'] = None
#                                 df_temp['longitude'] = None
#                             # 将结果添加到主 DataFrame
#                             df_main_v2 = pd.concat([df_main_v2, df_temp], ignore_index=True)

#     # 重新排序列
#     df_main_v2 = df_main_v2[['location_name', 'since', 'until', 'averageValue', 'latitude', 'longitude']]
#     df_main_v2.to_csv("air_data_realtime.csv", index=False)

#     return df_main_v2

# def preprocess_realtime_data(df):
#     # 处理提取的实时数据，按照日期和地区进行处理
#     df['until'] = pd.to_datetime(df['until'])
#     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d %H:%M:%S')  # 修改这里的日期格式
#     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
#     df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
#     df['location_id'] = df.index  # 添加 location_id 列，假设使用索引作为ID
#     df['value'] = df['BPM2.5']  # 添加 value 列，确保其值与 BPM2.5 列相同
#     df = df[['datetime_local', 'location_id', 'location_name', 'latitude', 'longitude', 'value']]  # 选择需要的列
#     return df

# def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
#     # 添加处理后的实时数据到空气质量文件
#     print("Realtime Data:")
#     print(df_realtime.head())  # 打印前几行数据
#     air_quality = pd.read_csv(air_quality_path)
#     air_quality = pd.concat([air_quality, df_realtime], ignore_index=True)
    
#     # 删除不需要的列
#     columns_to_keep = ['datetime_local', 'location_id', 'location_name', 'latitude', 'longitude', 'value']
#     air_quality = air_quality[columns_to_keep]
    
#     air_quality.to_csv("air_quality_preprocessed.csv", index=False)

# def print_air_quality_data(air_quality_path):
#     # 打印空气质量数据
#     air_quality = pd.read_csv(air_quality_path)
#     print("Air Quality Data:")
#     print(air_quality)

# if __name__ == '__main__':
#     realtime_data = main()
#     if realtime_data is not None:
#         realtime_data_processed = preprocess_realtime_data(realtime_data)
#         add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality_preprocessed.csv')
#         print_air_quality_data('air_quality_preprocessed.csv')


import requests
import json
import pandas as pd

def main():
    # 提取实时数据
    api_key = "ef4c5176645445238294a9fbf5fa8ad1"
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
        return None

    file_path = "real_time_data.json"

    # 记录数据
    with open(file_path, "w") as json_file:
        json.dump(response.json(), json_file)

    def json_to_dataframe(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        # 将 JSON 数组转换为 DataFrame
        df = pd.json_normalize(data['records'])
        return df
    
    # 调用函数以为df赋值
    df = json_to_dataframe(file_path)
    
    # 打印 DataFrame
    print(df)

    # 提取有用的信息
    column_1_data = df.iloc[:, 1]
    column_4_data = df.iloc[:, 4]
    column_6_data = df.iloc[:, 6]
    df_main_v2 = pd.DataFrame()
    for i, item in enumerate(column_4_data):
        if isinstance(item, float):
            continue  # 跳过 float 类型的数据
        
        if isinstance(item, list):
            for type in item: # 循环每种监控器类型读到的数据
                if type["name"] == 'PM2.5':
                    for tsr in type['timeSeriesReadings']: # 读取每种时间段的数据
                        tsr_name = tsr['timeSeriesName']
                        # 遍历 readings
                        for reading in tsr['readings']:
                            # 将每个 reading 转换为 DataFrame
                            df_temp = pd.DataFrame([reading])
                            # 添加 name 和 timeSeriesName 列
                            df_temp['location_name'] = column_1_data[i]
                            # 添加经度和纬度
                            if len(column_6_data[i]) >= 2:
                                df_temp['latitude'] = column_6_data[i][0]
                                df_temp['longitude'] = column_6_data[i][1]
                            else:
                                df_temp['latitude'] = None
                                df_temp['longitude'] = None
                            # 将结果添加到主 DataFrame
                            df_main_v2 = pd.concat([df_main_v2, df_temp], ignore_index=True)

    # 重新排序列
    df_main_v2 = df_main_v2[['location_name', 'since', 'until', 'averageValue', 'latitude', 'longitude']]
    df_main_v2.to_csv("air_data_realtime.csv", index=False)

    return df_main_v2

def preprocess_realtime_data(df):
    # 处理提取的实时数据，按照日期和地区进行处理
    df['until'] = pd.to_datetime(df['until'])
    df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d %H:%M:%S')  # 修改这里的日期格式
    df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
    df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
    df['location_id'] = df.index  # 添加 location_id 列，假设使用索引作为ID
    df['value'] = df['BPM2.5']  # 添加 value 列，确保其值与 BPM2.5 列相同
    df = df[['datetime_local', 'location_id', 'location_name', 'latitude', 'longitude', 'value']]  # 选择需要的列
    return df

def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
    # 添加处理后的实时数据到空气质量文件
    print("Realtime Data:")
    print(df_realtime.head())  # 打印前几行数据
    
    air_quality = pd.read_csv(air_quality_path)
    
    # 检查并处理 air_quality 数据的缺失值
    air_quality['value'] = air_quality['value'].fillna(air_quality.get('BPM2.5', air_quality['value']))

    # 删除不需要的列
    columns_to_keep = ['datetime_local', 'location_id', 'location_name', 'latitude', 'longitude', 'value']
    air_quality = air_quality[columns_to_keep]
    
    air_quality = pd.concat([air_quality, df_realtime], ignore_index=True)
    air_quality.to_csv("air_quality_preprocessed.csv", index=False)

def print_air_quality_data(air_quality_path):
    # 打印空气质量数据
    air_quality = pd.read_csv(air_quality_path)
    print("Air Quality Data:")
    print(air_quality)

if __name__ == '__main__':
    realtime_data = main()
    if realtime_data is not None:
        realtime_data_processed = preprocess_realtime_data(realtime_data)
        add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality.csv')
        print_air_quality_data('air_quality_preprocessed.csv')
