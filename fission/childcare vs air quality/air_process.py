# import pandas as pd

# # 读取air_quality.csv数据
# air_quality = pd.read_csv('air_quality.csv')

# # 检查数据的基本信息
# print(air_quality.info())

# # 处理缺失值：删除包含缺失值的行
# air_quality = air_quality.dropna()

# # 确保日期列的格式正确
# air_quality['datetime_AEST'] = pd.to_datetime(air_quality['datetime_AEST'], errors='coerce')
# air_quality['datetime_local'] = pd.to_datetime(air_quality['datetime_local'], errors='coerce')

# # 再次检查是否有无效日期并删除这些行
# air_quality = air_quality.dropna(subset=['datetime_AEST', 'datetime_local'])

# # 删除重复行
# air_quality = air_quality.drop_duplicates()

# # 确保其他列的数据类型正确
# air_quality['location_id'] = air_quality['location_id'].astype(int)
# air_quality['latitude'] = air_quality['latitude'].astype(float)
# air_quality['longitude'] = air_quality['longitude'].astype(float)
# air_quality['value'] = air_quality['value'].astype(float)

# # 检查并打印数据的描述性统计信息
# print(air_quality.describe())

# # 保存预处理后的数据到新的CSV文件
# air_quality.to_csv('air_quality_preprocessed.csv', index=False)

# print("预处理完成并保存为air_quality_preprocessed.csv")


import pandas as pd

# 读取air_quality.csv数据
air_quality = pd.read_csv('air_quality.csv')

# 检查数据的基本信息
print(air_quality.info())

# 只保留parameter_name为PM2.5的数据
air_quality = air_quality[air_quality['parameter_name'] == 'PM2.5']

# 处理缺失值：删除包含缺失值的行
air_quality = air_quality.dropna()

# 确保日期列的格式正确
air_quality['datetime_AEST'] = pd.to_datetime(air_quality['datetime_AEST'], errors='coerce')
air_quality['datetime_local'] = pd.to_datetime(air_quality['datetime_local'], errors='coerce')

# 再次检查是否有无效日期并删除这些行
air_quality = air_quality.dropna(subset=['datetime_AEST', 'datetime_local'])

# 删除重复行
air_quality = air_quality.drop_duplicates()

# 确保其他列的数据类型正确
air_quality['location_id'] = air_quality['location_id'].astype(int)
air_quality['latitude'] = air_quality['latitude'].astype(float)
air_quality['longitude'] = air_quality['longitude'].astype(float)
air_quality['value'] = air_quality['value'].astype(float)

# 检查并打印数据的描述性统计信息
print(air_quality.describe())

# 保存预处理后的数据到新的CSV文件
air_quality.to_csv('air_quality_preprocessed.csv', index=False)

print("预处理完成并保存为air_quality_preprocessed.csv")
