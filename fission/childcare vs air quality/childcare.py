import json
import requests
import pandas as pd
def getChildCare():
    def process_data(df):
        columns_drop = ['service_approval_number', ' date_approval_granted', ' geocode_level',
       ' trading_name', ' provider_approval_number', ' state', 
       ' conditions']
    #     ,
    #    ' longitude', ' latitude']
        df.drop(columns_drop, axis=1, inplace=True)
        contains_nas = df.isna().any(axis=1)
        df_clean = df[~contains_nas]
        return df_clean

    path = 'd1/acecqa_approved_providers_2017-3999629755719231428.csv'
    df = pd.read_csv(path)
    df_clean = process_data(df)
    output_path = './child_care.csv'
    df_clean.to_csv(output_path, encoding='utf-8', index=False)
    print(df_clean.head())  # 输出前5行数据以查看数据格式
getChildCare()

