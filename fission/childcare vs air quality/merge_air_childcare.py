
import pandas as pd
from geopy.distance import geodesic

# 读取第一个数据集（child_care.csv）
child_care = pd.read_csv('child_care.csv')

# 去除列名中的前导和尾随空格
child_care.columns = child_care.columns.str.strip()

# 打印 child_care 数据集的列名
print("Child care columns:", child_care.columns)

# 读取预处理后的第二个数据集（air_quality_preprocessed.csv）
air_quality = pd.read_csv('air_quality_preprocessed.csv')

# 创建一个地理位置的 DataFrame 用于匹配
locations = air_quality[['location_name', 'latitude', 'longitude']].drop_duplicates()

# 计算所有 location_name 的空气质量值 (value) 的平均值
average_air_quality = air_quality.groupby('location_name')['value'].mean().reset_index()
average_air_quality.rename(columns={'value': 'avg_air_quality'}, inplace=True)

# 合并平均空气质量数据和地理位置数据
location_avg_quality = pd.merge(locations, average_air_quality, on='location_name', how='left')

# 定义一个函数来找到最近的地点
def find_nearest_air_quality(lat, lon, locations_df):
    distances = locations_df.apply(lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).meters, axis=1)
    nearest_location = locations_df.loc[distances.idxmin()]
    return nearest_location['avg_air_quality']

# 检查 child_care 数据集中是否包含 'latitude' 和 'longitude' 列
if 'latitude' in child_care.columns and 'longitude' in child_care.columns:
    # 为 child_care 数据集中的每一行找到最近的空气质量值
    child_care['avg_air_quality'] = child_care.apply(
        lambda row: find_nearest_air_quality(row['latitude'], row['longitude'], location_avg_quality), axis=1)
else:
    print("Error: 'latitude' and 'longitude' columns not found in child_care dataset.")
    # 如果列名不同，请替换为正确的列名，例如:
    # child_care['avg_air_quality'] = child_care.apply(
    #     lambda row: find_nearest_air_quality(row['actual_latitude_column'], row['actual_longitude_column'], location_avg_quality), axis=1)

# 保存合并后的数据到新的 CSV 文件
child_care.to_csv('child_care_with_air_quality.csv', index=False)

print("合并完成并保存为 child_care_with_air_quality.csv")





# import pandas as pd
# from geopy.distance import geodesic

# # 读取第一个数据集（child_care.csv）
# child_care = pd.read_csv('child_care.csv')

# # 去除列名中的前导和尾随空格
# child_care.columns = child_care.columns.str.strip()

# # 打印 child_care 数据集的列名
# print("Child care columns:", child_care.columns)

# # 读取预处理后的第二个数据集（air_quality_preprocessed.csv）
# air_quality = pd.read_csv('air_quality_preprocessed.csv')

# # 创建一个地理位置的 DataFrame 用于匹配
# locations = air_quality[['location_name', 'latitude', 'longitude']].drop_duplicates()

# # 计算所有 location_name 的空气质量值 (value) 的平均值
# average_air_quality = air_quality.groupby('location_name')['value'].mean().reset_index()
# average_air_quality.rename(columns={'value': 'avg_air_quality'}, inplace=True)

# # 合并平均空气质量数据和地理位置数据
# location_avg_quality = pd.merge(locations, average_air_quality, on='location_name', how='left')

# # 定义一个函数来找到最近的地点
# def find_nearest_air_quality(lat, lon, locations_df):
#     distances = locations_df.apply(lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).meters, axis=1)
#     nearest_location = locations_df.loc[distances.idxmin()]
#     return nearest_location['avg_air_quality']

# # 判断数据是否为 2024 年及以后的，并根据情况取值
# def get_air_quality_value(row):
#     if pd.to_datetime(row['datetime_local']).year >= 2024:
#         return row['BPM2.5']
#     else:
#         return row['value']

# # 为 child_care 数据集中的每一行找到最近的空气质量值
# child_care['avg_air_quality'] = child_care.apply(
#     lambda row: find_nearest_air_quality(row['latitude'], row['longitude'], location_avg_quality), axis=1)

# # 添加对日期的判断并取值
# air_quality['datetime_local'] = pd.to_datetime(air_quality['datetime_local'])
# air_quality['air_quality_value'] = air_quality.apply(get_air_quality_value, axis=1)

# # 计算所有 location_name 的空气质量值 (value) 的平均值
# average_air_quality = air_quality.groupby('location_name')['air_quality_value'].mean().reset_index()
# average_air_quality.rename(columns={'air_quality_value': 'avg_air_quality'}, inplace=True)

# # 合并平均空气质量数据和地理位置数据
# location_avg_quality = pd.merge(locations, average_air_quality, on='location_name', how='left')

# # 为 child_care 数据集中的每一行找到最近的空气质量值
# child_care['avg_air_quality'] = child_care.apply(
#     lambda row: find_nearest_air_quality(row['latitude'], row['longitude'], location_avg_quality), axis=1)

# # 保存合并后的数据到新的 CSV 文件
# child_care.to_csv('child_care_with_air_quality.csv', index=False)

# print("合并完成并保存为 child_care_with_air_quality.csv")




