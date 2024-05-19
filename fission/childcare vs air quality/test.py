# import requests
# import json
# import pandas as pd

# import os 
# def main():
#     def addIn_merge(path_air, realtime_air_df):
#         # if file exist, append
#         if os.path.exists(path_air):
#             with open('path', 'r+') as file:
#                 exisiting_data = pd.read_json(file)
#                 combine_data = pd.concat([exisiting_data, realtime_air_df], ignore_index=True)
#                 combine_data.to_json(path_air)
#         # if not comvert df to json
#         else:
#             realtime_air_df.to_json(path_air)

#     # extract mel 1 hour data from real time data
#     def find_mel_1hr_data(air_data):
#         melbourne_cities = [
#             'Box Hill',
#             'Alphington',
#             'Dandenong',
#             'Point Cook',
#             'Melbourne CBD',
#             'Brighton',
#             'Altona North',
#             'Healesville',
#             'Sunbury',
#             'Macleod',
#             'Spotswood',
#             'Kingsville',
#             'Melton',
#             'Mooroolbark',
#             'Footscray',
#             'Brooklyn'
#         ]
        
#         filtered_df = air_data[air_data['timeSeriesName'] == '1HR_AV']
#         mel_df = filtered_df[filtered_df['sit_name'].isin(melbourne_cities)]

#         return mel_df

#     # preprocess the extracted data
#     def preprocess_new_air(df):
#         air_data = df

#         target_cols = ['sit_name', 'until', 'averageValue']
#         air_data2 = air_data.filter(items=target_cols)

#         air_data2['until'] = pd.to_datetime(air_data2['until'])
#         air_data2['datetime_local'] = air_data2['until'].dt.strftime('%Y-%m-%d-%H')


#         # Change col name
#         air_data2 = air_data2.rename(columns={'sit_name': 'location_name'})
#         air_data2 = air_data2.rename(columns={'averageValue': 'BPM2.5'})

#         # change col order
#         new_order = ['datetime_local', 'location_name', 'BPM2.5']
#         air_data2 = air_data2.reindex(columns=new_order)
#         air_data2 = air_data2.dropna(subset=['BPM2.5'])
#         # air_data2.drop(columns=['until'], inplace=True)

#         bpm25_mean = air_data2['BPM2.5'].mean()
#         datetime_local = air_data2.iloc[0, 0]

#         mel_air = pd.DataFrame({
#             'datetime_local': [datetime_local],
#             'location_name': ['Melbourne'],
#             'BPM2.5': [bpm25_mean]
#         })

#         return mel_air
#     # Extract real time data
#     api_key = "ef4c5176645445238294a9fbf5fa8ad1"
#     subscription_name = "comp90024"
#     url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/parameters?environmentalSegment=air"

#     headers = {
#         "User-Agent": 'curl/8.4.0',
#         "Cache-Contrl": "no-cache",
#         'X-API-Key': api_key
#     }


#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
            
#     else:
#         print("query fail:", response.status_code)







#     file_path = "real_time_data.json"

#     # record data
#     with open(file_path, "w") as json_file:
#         json.dump(response.json(), json_file)


#     def json_to_dataframe(file_path):
#         with open(file_path, 'r') as file:
#             data = json.load(file)

#         # 将JSON数组转换为DataFrame
#         df = pd.json_normalize(data['records'])

        
#         return df


#     df = json_to_dataframe(file_path)

#     # 提取有用的信息
#     column_0_data = df.iloc[:, 0]
#     column_1_data = df.iloc[:, 1]
#     column_4_data = df.iloc[:, 4]
#     df_main_v2 = pd.DataFrame()
#     for i, item in enumerate(column_4_data):
#         if isinstance(item, float):
            
#             continue  # 跳过 float 类型的数据
        
#         if isinstance(item, list) :
#             for type in item: #循环每种监控器类型读到的数据
#                 if type["name"] ==  'PM2.5':
#                     for tsr in type['timeSeriesReadings']: # 读取每种时间段的数据
#                         tsr_name = tsr['timeSeriesName']
#                         # 遍历 readings
#                         for reading in tsr['readings']:
#                             # 将每个 reading 转换为 DataFrame
#                             df_temp = pd.DataFrame([reading])
#                             # 添加 name 和 timeSeriesName 列
#                             df_temp['name'] = 'PM2.5'
#                             df_temp['timeSeriesName'] = tsr_name
#                             df_temp['sit_id'] = column_0_data[i]
#                             df_temp['sit_name'] = column_1_data[i]
#                             # 将结果添加到主 DataFrame
#                             df_main_v2 = pd.concat([df_main_v2, df_temp])

#     # 重新排序列
#     df_main_v2 = df_main_v2[['sit_id','sit_name', 'name', 'timeSeriesName', 'since', 'until', 'averageValue', 'unit', 'confidence', 'totalSample', 'healthAdvice', 'healthAdviceColor', 'healthCode']]

#     df_main_v2.to_csv("air_data_realtime.csv", index=False)

#     realtime_air_1h = find_mel_1hr_data(df_main_v2)
#     realtime_air_df = preprocess_new_air(realtime_air_1h)
#     print(realtime_air_df)
#     path_air = "realTime_1h_air_data.json"
#     # addIn_merge(path_air, realtime_air_df)


    
# if __name__ == '__main__':
#     print(main())

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

#     df = json_to_dataframe(file_path)

#     # 提取有用的信息
#     column_0_data = df.iloc[:, 0]
#     column_1_data = df.iloc[:, 1]
#     column_4_data = df.iloc[:, 4]
#     df_main_v2 = pd.DataFrame()
#     for i, item in enumerate(column_4_data):
#         if isinstance(item, float):
#             continue  # 跳过 float 类型的数据
        
#         if isinstance(item, list) :
#             for type in item: # 循环每种监控器类型读到的数据
#                 if type["name"] ==  'PM2.5':
#                     for tsr in type['timeSeriesReadings']: # 读取每种时间段的数据
#                         tsr_name = tsr['timeSeriesName']
#                         # 遍历 readings
#                         for reading in tsr['readings']:
#                             # 将每个 reading 转换为 DataFrame
#                             df_temp = pd.DataFrame([reading])
#                             # 添加 name 和 timeSeriesName 列
#                             df_temp['name'] = 'PM2.5'
#                             df_temp['timeSeriesName'] = tsr_name
#                             df_temp['sit_id'] = column_0_data[i]
#                             df_temp['sit_name'] = column_1_data[i]
#                             # 将结果添加到主 DataFrame
#                             df_main_v2 = pd.concat([df_main_v2, df_temp])

#     # 重新排序列
#     df_main_v2 = df_main_v2[['sit_id','sit_name', 'name', 'timeSeriesName', 'since', 'until', 'averageValue', 'unit', 'confidence', 'totalSample', 'healthAdvice', 'healthAdviceColor', 'healthCode']]
#     df_main_v2.to_csv("air_data_realtime.csv", index=False)

#     return df_main_v2


# def preprocess_realtime_data(df):
#     # 处理提取的实时数据，按照日期和地区进行处理
#     df['until'] = pd.to_datetime(df['until'])
#     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d-%H')
#     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
#     df = df[['datetime_local', 'location_name', 'BPM2.5']]
#     return df


# def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
#     # 添加处理后的实时数据到空气质量文件
#     air_quality = pd.read_csv(air_quality_path)
#     air_quality = pd.concat([air_quality, df_realtime], ignore_index=True)
#     air_quality.to_csv(air_quality_path, index=False)

# def print_air_quality_data(air_quality_path):
#     # 打印空气质量数据
#     air_quality = pd.read_csv(air_quality_path)
#     print("Air Quality Data:")
#     print(air_quality)

# if __name__ == '__main__':
#     realtime_data = main()
#     realtime_data_processed = preprocess_realtime_data(realtime_data)
#     add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality.csv')
#     print_air_quality_data('air_quality.csv')



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

#     df = json_to_dataframe(file_path)

#     # 提取有用的信息
#     # column_0_data = df.iloc[:, 0]
#     # column_1_data = df.iloc[:, 1]
#     # column_4_data = df.iloc[:, 4]
#     # df_main_v2 = pd.DataFrame()
#     # 提取有用的信息
#     df_main_v2 = df.copy()

#     for i, item in enumerate(column_4_data):
#         if isinstance(item, float):
#             continue  # 跳过 float 类型的数据
        
#         if isinstance(item, list) :
#             for type in item: # 循环每种监控器类型读到的数据
#                 if type["name"] ==  'PM2.5':
#                     for tsr in type['timeSeriesReadings']: # 读取每种时间段的数据
#                         tsr_name = tsr['timeSeriesName']
#                         # 遍历 readings
#                         for reading in tsr['readings']:
#                             # 将每个 reading 转换为 DataFrame
#                             df_temp = pd.DataFrame([reading])
#                             # 添加 name 和 timeSeriesName 列
#                             df_temp['name'] = 'PM2.5'
#                             df_temp['timeSeriesName'] = tsr_name
#                             df_temp['sit_id'] = column_0_data[i]
#                             df_temp['sit_name'] = column_1_data[i]
#                             # 将结果添加到主 DataFrame
#                             df_main_v2 = pd.concat([df_main_v2, df_temp])

#     # 重新排序列
#     df_main_v2 = df_main_v2[['sit_id','sit_name', 'name', 'timeSeriesName', 'since', 'until', 'averageValue', 'unit', 'confidence', 'totalSample', 'healthAdvice', 'healthAdviceColor', 'healthCode']]
    
#     # 添加经纬度信息
#     location_dict = {
#         "Morwell East": {
#             "latitude": -38.229393,
#             "longitude": 146.424454
#         },
#         "Altona North": {
#             "latitude": -37.84455,
#             "longitude": 144.8629
#         },
#         "Dandenong": {
#             "latitude": -37.98576,
#             "longitude": 145.1987
#         },
#         "Point Cook": {
#             "latitude": -37.9263153,
#             "longitude": 144.7567
#         },
#         "Brooklyn": {
#             "latitude": -37.8220978,
#             "longitude": 144.8471
#         },
#         "Geelong South": {
#             "latitude": -38.17356,
#             "longitude": 144.3703
#         },
#         "Mooroolbark": {
#             "latitude": -37.7749672,
#             "longitude": 145.3285
#         },
#         "Footscray": {
#             "latitude": -37.803709,
#             "longitude": 144.869342
#         },
#         "Traralgon": {
#             "latitude": -38.1942825,
#             "longitude": 146.531464
#         },
#         "Alphington": {
#             "latitude": -37.7784081,
#             "longitude": 145.0306
#         },
#         "Churchill": {
#             "latitude": -38.3043137,
#             "longitude": 146.414932
#         },
#         "Moe": {
#             "latitude": -38.1864662,
#             "longitude": 146.258331
#         },
#         "Newborough": {
#             "latitude": -38.18772,
#             "longitude": 146.2927
#         },
#         "Melton": {
#             "latitude": -37.7064552,
#             "longitude": 144.5669
#         }
#     }
#     df_main_v2['latitude'] = df_main_v2['sit_name'].map(lambda x: location_dict[x]['latitude'] if x in location_dict else None)
#     df_main_v2['longitude'] = df_main_v2['sit_name'].map(lambda x: location_dict[x]['longitude'] if x in location_dict else None)

#     # 将最后一列数字值添加到 'value' 列
#     df_main_v2['value'] = df_main_v2.iloc[:, -2]

#     # 保存到 CSV 文件
#     df_main_v2.to_csv("air_data_realtime.csv", index=False)

#     return df_main_v2


# def preprocess_realtime_data(df):
#     # 处理提取的实时数据，按照日期和地区进行处理
#     df['until'] = pd.to_datetime(df['until'])
#     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d-%H')
#     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
#     df = df[['datetime_local', 'location_name', 'BPM2.5']]
#     return df


# def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
#     # 添加处理后的实时数据到空气质量文件
#     air_quality = pd.read_csv(air_quality_path)
#     air_quality = pd.concat([air_quality, df_realtime], ignore_index=True)
#     air_quality.to_csv(air_quality_path, index=False)

# def print_air_quality_data(air_quality_path):
#     # 打印空气质量数据
#     air_quality = pd.read_csv(air_quality_path)
#     print("Air Quality Data:")
#     print(air_quality)

# if __name__ == '__main__':
#     realtime_data = main()
#     realtime_data_processed = preprocess_realtime_data(realtime_data)
#     add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality.csv')
#     print_air_quality_data('air_quality.csv')












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

#     df = json_to_dataframe(file_path)

#     # 提取有用的信息
#     column_0_data = df.iloc[:, 0]
#     column_1_data = df.iloc[:, 1]
#     column_4_data = df.iloc[:, 4]
#     column_6_data = df.iloc[:, 6]
#     df_main_v2 = pd.DataFrame()
#     for i, item in enumerate(column_4_data):
#         if isinstance(item, float):
#             continue  # 跳过 float 类型的数据
        
#         if isinstance(item, list) :
#             for type in item: # 循环每种监控器类型读到的数据
#                 if type["name"] ==  'PM2.5':
#                     for tsr in type['timeSeriesReadings']: # 读取每种时间段的数据
#                         tsr_name = tsr['timeSeriesName']
#                         # 遍历 readings
#                         for reading in tsr['readings']:
#                             # 将每个 reading 转换为 DataFrame
#                             df_temp = pd.DataFrame([reading])
#                             # 添加 name 和 timeSeriesName 列
#                             df_temp['name'] = 'PM2.5'
#                             df_temp['timeSeriesName'] = tsr_name
#                             df_temp['sit_id'] = column_0_data[i]
#                             df_temp['sit_name'] = column_1_data[i]
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
#     df_main_v2 = df_main_v2[['sit_id','sit_name', 'name', 'timeSeriesName', 'since', 'until', 'averageValue', 'unit', 'confidence', 'totalSample', 'healthAdvice', 'healthAdviceColor', 'healthCode', 'latitude', 'longitude']]
#     df_main_v2.to_csv("air_data_realtime.csv", index=False)

#     return df_main_v2

# def preprocess_realtime_data(df):
#     # 处理提取的实时数据，按照日期和地区进行处理
#     df['until'] = pd.to_datetime(df['until'])
#     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d-%H')
#     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
#     df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
#     return df



# def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
#     # 添加处理后的实时数据到空气质量文件
#     print("Realtime Data:")
#     print(df_realtime.head())  # 打印前几行数据
#     air_quality = pd.read_csv(air_quality_path)
#     air_quality = pd.concat([air_quality, df_realtime], ignore_index=True)
#     air_quality['latitude'] = df_realtime['latitude']
#     air_quality['longitude'] = df_realtime['longitude']
#     air_quality.to_csv(air_quality_path, index=False)




# def print_air_quality_data(air_quality_path):
#     # 打印空气质量数据
#     air_quality = pd.read_csv(air_quality_path)
#     print("Air Quality Data:")
#     print(air_quality)

# if __name__ == '__main__':
#     realtime_data = main()
#     realtime_data_processed = preprocess_realtime_data(realtime_data)
#     add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality.csv')
#     print_air_quality_data('air_quality.csv')


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

#     df = json_to_dataframe(file_path)

#     # 提取有用的信息
#     column_0_data = df.iloc[:, 0]
#     column_1_data = df.iloc[:, 1]
#     column_4_data = df.iloc[:, 4]
#     column_6_data = df.iloc[:, 6]
#     df_main_v2 = pd.DataFrame()
#     for i, item in enumerate(column_4_data):
#         if isinstance(item, float):
#             continue  # 跳过 float 类型的数据
        
#         if isinstance(item, list) :
#             for type in item: # 循环每种监控器类型读到的数据
#                 if type["name"] ==  'PM2.5':
#                     for tsr in type['timeSeriesReadings']: # 读取每种时间段的数据
#                         tsr_name = tsr['timeSeriesName']
#                         # 遍历 readings
#                         for reading in tsr['readings']:
#                             # 将每个 reading 转换为 DataFrame
#                             df_temp = pd.DataFrame([reading])
#                             # 添加 name 和 timeSeriesName 列
#                             df_temp['name'] = 'PM2.5'
#                             df_temp['timeSeriesName'] = tsr_name
#                             df_temp['sit_id'] = column_0_data[i]
#                             df_temp['sit_name'] = column_1_data[i]
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
#     df_main_v2 = df_main_v2[['sit_id','sit_name', 'name', 'timeSeriesName', 'since', 'until', 'averageValue', 'unit', 'confidence', 'totalSample', 'healthAdvice', 'healthAdviceColor', 'healthCode', 'latitude', 'longitude']]
#     df_main_v2.to_csv("air_data_realtime.csv", index=False)

#     return df_main_v2


# def preprocess_realtime_data(df):
#     # 处理提取的实时数据，按照日期和地区进行处理
#     df['until'] = pd.to_datetime(df['until'])
#     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d-%H')
#     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
#     df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
#     return df


# def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
#     # 添加处理后的实时数据到空气质量文件
#     print("Realtime Data:")
#     print(df_realtime.head())  # 打印前几行数据
#     air_quality = pd.read_csv(air_quality_path)
#     air_quality = pd.merge(air_quality, df_realtime, on=['datetime_local', 'location_name'], how='outer')
#     air_quality.to_csv(air_quality_path, index=False)


# def print_air_quality_data(air_quality_path):
#     # 打印空气质量数据
#     air_quality = pd.read_csv(air_quality_path)
#     print("Air Quality Data:")
#     print(air_quality)

# if __name__ == '__main__':
#     realtime_data = main()
#     realtime_data_processed = preprocess_realtime_data(realtime_data)
#     add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality.csv')
#     print_air_quality_data('air_quality.csv')




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

#     df = json_to_dataframe(file_path)

#     # 提取有用的信息
#     column_1_data = df.iloc[:, 1]
#     column_4_data = df.iloc[:, 4]
#     column_6_data = df.iloc[:, 6]
#     df_main_v2 = pd.DataFrame()
#     for i, item in enumerate(column_4_data):
#         if isinstance(item, float):
#             continue  # 跳过 float 类型的数据
        
#         if isinstance(item, list) :
#             for type in item: # 循环每种监控器类型读到的数据
#                 if type["name"] ==  'PM2.5':
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
#     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d-%H')
#     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
#     df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
#     return df


# def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
#     # 添加处理后的实时数据到空气质量文件
#     print("Realtime Data:")
#     print(df_realtime.head())  # 打印前几行数据
#     air_quality = pd.read_csv(air_quality_path)
#     air_quality = pd.concat([air_quality, df_realtime], ignore_index=True)
#     air_quality.to_csv(air_quality_path, index=False)


# def print_air_quality_data(air_quality_path):
#     # 打印空气质量数据
#     air_quality = pd.read_csv(air_quality_path)
#     print("Air Quality Data:")
#     print(air_quality)

# if __name__ == '__main__':
#     realtime_data = main()
#     realtime_data_processed = preprocess_realtime_data(realtime_data)
#     add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality.csv')
#     print_air_quality_data('air_quality.csv')

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

#     df = json_to_dataframe(file_path)

#     # 提取有用的信息
#     column_1_data = df.iloc[:, 1]
#     column_4_data = df.iloc[:, 4]
#     column_6_data = df.iloc[:, 6]
#     df_main_v2 = pd.DataFrame()
#     for i, item in enumerate(column_4_data):
#         if isinstance(item, float):
#             continue  # 跳过 float 类型的数据
        
#         if isinstance(item, list) :
#             for type in item: # 循环每种监控器类型读到的数据
#                 if type["name"] ==  'PM2.5':
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


# # def preprocess_realtime_data(df):
# #     # 处理提取的实时数据，按照日期和地区进行处理
# #     df['until'] = pd.to_datetime(df['until'])
# #     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d-%H')
# #     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
# #     df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
# #     return df

# def preprocess_realtime_data(df):
#     # 处理提取的实时数据，按照日期和地区进行处理
#     df['until'] = pd.to_datetime(df['until'])
#     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d %H:%M:%S')  # 修改这里的日期格式
#     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
#     df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
#     return df



# def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
#     # 添加处理后的实时数据到空气质量文件
#     print("Realtime Data:")
#     print(df_realtime.head())  # 打印前几行数据
#     air_quality = pd.read_csv(air_quality_path)
#     air_quality = pd.concat([air_quality, df_realtime], ignore_index=True)
#     air_quality.to_csv("air_quality_preprocessed.csv", index=False)


# def print_air_quality_data(air_quality_path):
#     # 打印空气质量数据
#     air_quality = pd.read_csv(air_quality_path)
#     print("Air Quality Data:")
#     print(air_quality)

# if __name__ == '__main__':
#     realtime_data = main()
#     realtime_data_processed = preprocess_realtime_data(realtime_data)
#     add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality.csv')
#     print_air_quality_data('air_quality.csv')

import requests
import json
import pandas as pd

def main():
    # 提取实时数据
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

    df = json_to_dataframe(file_path)

    # 提取有用的信息
    column_1_data = df.iloc[:, 1]
    column_4_data = df.iloc[:, 4]
    column_6_data = df.iloc[:, 6]
    df_main_v2 = pd.DataFrame()
    for i, item in enumerate(column_4_data):
        if isinstance(item, float):
            continue  # 跳过 float 类型的数据
        
        if isinstance(item, list) :
            for type in item: # 循环每种监控器类型读到的数据
                if type["name"] ==  'PM2.5':
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


# def preprocess_realtime_data(df):
#     # 处理提取的实时数据，按照日期和地区进行处理
#     df['until'] = pd.to_datetime(df['until'])
#     df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d-%H')
#     df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
#     df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
#     return df

def preprocess_realtime_data(df):
    # 处理提取的实时数据，按照日期和地区进行处理
    df['until'] = pd.to_datetime(df['until'])
    df['datetime_local'] = df['until'].dt.strftime('%Y-%m-%d %H:%M:%S')  # 修改这里的日期格式
    df = df.rename(columns={'sit_name': 'location_name', 'averageValue': 'BPM2.5'})
    df = df[['datetime_local', 'location_name', 'BPM2.5', 'latitude', 'longitude']]  # 保留经度和纬度列
    return df



def add_realtime_data_to_air_quality(df_realtime, air_quality_path):
    # 添加处理后的实时数据到空气质量文件
    print("Realtime Data:")
    print(df_realtime.head())  # 打印前几行数据
    air_quality = pd.read_csv(air_quality_path)
    air_quality = pd.concat([air_quality, df_realtime], ignore_index=True)
    # 添加值的处理，确保新数据的 value 列与 BPM2.5 列相同
    air_quality['value'] = air_quality['BPM2.5']
    air_quality.to_csv("air_quality_preprocessed.csv", index=False)


def print_air_quality_data(air_quality_path):
    # 打印空气质量数据
    air_quality = pd.read_csv(air_quality_path)
    print("Air Quality Data:")
    print(air_quality)

if __name__ == '__main__':
    realtime_data = main()
    realtime_data_processed = preprocess_realtime_data(realtime_data)
    add_realtime_data_to_air_quality(realtime_data_processed, 'air_quality.csv')
    print_air_quality_data('air_quality.csv')
