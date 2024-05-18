# import json
# import requests
# import pandas as pd

# def getRealEstateData(url, path):
#     def process_data(df1, df2):
#         # clean json data
#         columns_drop = ['location', 'property_id', 'base_property_id', 'dwelling_number','longitude', 'latitude','census_year']
#         df1.drop(columns_drop, axis=1, inplace=True)

#         #merge two data
#         df1['geography_name'] = df1['building_address'].str.slice(start=-4)
#         df2['geography_name'] = df2['geography_name'].astype(str)
#         merged_df = pd.merge(df1, df2,  on='geography_name', how='inner')

#         #remove na values       
#         contains_nas = merged_df.isna().any(axis=1)
#         df_clean = merged_df[~contains_nas]

#         df_clean.to_csv('.path/final_data.csv', encoding='utf-8', index=False)

#     def download_data(url):
#         response = requests.get(url)
#         if response.status_code == 200:
#             with open('data.csv', 'wb') as file:
#                 file.write(response.content)
#                 print("CSV downloaded successfully")
#         else:
#             print(f"Failed，Status code：{response.status_code}")

    
    
#     with open('d1/residential-dwellings.json', 'r') as file:
#         df1 = json.load(file)
#     df1 = pd.DataFrame(df1)
#     download_data(url)
#     csv_path = 'affordability.csv'
#     df2 = pd.read_csv(csv_path, encoding='utf-8')
#     process_data(df1, df2)

# url = 'https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/residential-dwellings/exports/csv?delimiter=%2C'
# path = './'
# getRealEstateData(url, path)



# import os
# import json
# import requests
# import pandas as pd

# def getRealEstateData(url, path):
#     def process_data(df1, df2):
#         # 清理 JSON 数据
#         columns_drop = ['location', 'property_id', 'base_property_id', 'dwelling_number', 'longitude', 'latitude', 'census_year']
#         df1.drop(columns_drop, axis=1, inplace=True)

#         # 合并两个数据
#         df1['geography_name'] = df1['building_address'].str.slice(start=-4)
#         df2['geography_name'] = df2['geography_name'].astype(str)
#         merged_df = pd.merge(df1, df2, on='geography_name', how='inner')

#         # 移除 NA 值
#         contains_nas = merged_df.isna().any(axis=1)
#         df_clean = merged_df[~contains_nas]

#         # 确保目标目录存在
#         output_dir = path
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)

#         # 保存清理后的数据
#         output_file = os.path.join(output_dir, 'final_data.csv')
#         df_clean.to_csv(output_file, encoding='utf-8', index=False)
#         print(f"Data successfully saved to {output_file}")

#         print("Sample of the final data:")
#         print(df_clean.head())


#     def download_data(url):
#         response = requests.get(url)
#         if response.status_code == 200:
#             with open('data.csv', 'wb') as file:
#                 file.write(response.content)
#                 print("CSV downloaded successfully")
#         else:
#             print(f"Failed, Status code: {response.status_code}")

#     # 读取 JSON 文件
#     with open('d1/residential-dwellings.json', 'r') as file:
#         df1 = json.load(file)
#     df1 = pd.DataFrame(df1)

#     # 下载 CSV 文件
#     download_data(url)
#     csv_path = 'affordability.csv'
#     df2 = pd.read_csv(csv_path, encoding='utf-8')

#     # 处理数据
#     process_data(df1, df2)

# # 设置 URL 和路径
# url = 'https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/residential-dwellings/exports/csv?delimiter=%2C'
# path = './path'  # 确保这个路径存在或可以被创建

# # 调用函数
# getRealEstateData(url, path)


import os
import json
import requests
import pandas as pd

def getRealEstateData(url, path):
    def process_data(df1, df2):
        # 清理 JSON 数据
        columns_drop = ['location', 'property_id', 'base_property_id', 'dwelling_number', 'longitude', 'latitude', 'census_year']
        df1.drop(columns_drop, axis=1, inplace=True)

        # 合并两个数据
        df1['geography_name'] = df1['building_address'].str.slice(start=-4)
        df2['geography_name'] = df2['geography_name'].astype(str)
        merged_df = pd.merge(df1, df2, on='geography_name', how='inner')

        # 移除 NA 值
        contains_nas = merged_df.isna().any(axis=1)
        df_clean = merged_df[~contains_nas]

        # 确保目标目录存在
        output_dir = path
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 保存清理后的数据为 JSON 格式
        output_file = os.path.join(output_dir, 'final_data.json')
        df_clean.to_json(output_file, orient='records', lines=True)
        print(f"Data successfully saved to {output_file}")

        print("Sample of the final data:")
        print(df_clean.head())


    def download_data(url):
        response = requests.get(url)
        if response.status_code == 200:
            with open('data.csv', 'wb') as file:
                file.write(response.content)
                print("CSV downloaded successfully")
        else:
            print(f"Failed, Status code: {response.status_code}")

    # 读取 JSON 文件
    with open('d1/residential-dwellings.json', 'r') as file:
        df1 = json.load(file)
    df1 = pd.DataFrame(df1)

    # 下载 CSV 文件
    download_data(url)
    csv_path = 'affordability.csv'
    df2 = pd.read_csv(csv_path, encoding='utf-8')

    # 处理数据
    process_data(df1, df2)

# 设置 URL 和路径
url = 'https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/residential-dwellings/exports/csv?delimiter=%2C'
path = './path'  # 确保这个路径存在或可以被创建

# 调用函数
getRealEstateData(url, path)
