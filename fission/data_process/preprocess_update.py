import pandas as pd
import json 



def preprocess_dataframe(df):
    # 将日期时间列转换为日期，并丢弃时间部分
    
    df['datetime_local'] = pd.to_datetime(df['datetime_local'])
    df['datetime_local'] = df['datetime_local'].dt.strftime('%Y-%m-%d-%H')
    # 根据日期进行分组，并计算每天的平均bpm2.5值
    new_df = df.groupby(['datetime_local', 'location_name'])['BPM2.5'].mean().reset_index()
    new_df2 = new_df.dropna()
    return new_df2



#####################################################################################
# handle new air data
# extract mel 1 hour data from real time data
def find_mel_1hr_data(air_data):
    
    filtered_df = air_data [air_data ['timeSeriesName'] == '1HR_AV']
    mel_df = filtered_df[filtered_df['sit_name'] == 'Melbourne CBD']
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
    
    # air_data2.drop(columns=['until'], inplace=True)

    return air_data2

# add the new data to the static data set
def concate_new_with_old(df, old_df):
    new_df =  preprocess_new_air(df)
    concatenated_df = pd.concat([old_df, new_df], axis=0, ignore_index=True)
    return concatenated_df

###########################################################################################
def clean_weather_data(df):
    columns_drop = ['weather', 'swell_height', 'sea_state', 'swell_period', 'press_tend',
                     'swell_dir_worded', 'wmo', 'history_product', 'cloud_base_m', 'cloud_oktas', 
                     'cloud', 'cloud_type_id', 'cloud_type', 'aifstime_utc', 'local_date_time', 'sort_order', 'vis_km', 'rain_trace']
    df_cleaned = df.drop(columns = columns_drop)
    df_cleaned['name'] = 'Melbourne CBD'

    # 将 datetime 格式转换为 'YYYY-MM-DD' 格式
    df_cleaned['local_date_time_full'] = pd.to_datetime(df_cleaned['local_date_time_full'], format='%Y%m%d%H%M%S')
    df_cleaned['local_date_time_full'] = df_cleaned['local_date_time_full'].dt.strftime('%Y-%m-%d-%H')

    #这个是为了确保没有半个小时的数据出现
    if df_cleaned.iloc[0]['local_date_time_full'] != df_cleaned.iloc[1]['local_date_time_full']:
        df_cleaned = df_cleaned.drop(0)

    return df_cleaned

# 假设都进来的数据包括了当日的历史记录
def bom_first_two(realtime_df):
    first_two_rows = realtime_df.head(2)
    df = clean_weather_data(first_two_rows)
    # 将前两行数据附加到同一文件中
    # df.to_csv(filename, mode='a', header=False, index=False)
    return df


def combine_1h(df_mel_v2):
    mask = df_mel_v2['local_date_time_full'].shift(-1) == df_mel_v2['local_date_time_full']
    processed_df = pd.DataFrame(columns=df_mel_v2.columns)

    # 对于连续的行，将其他列的值进行合并或者求平均
    rows_to_append = []
    for idx, row in df_mel_v2[mask].iterrows():
        if idx + 1 < len(df_mel_v2):
            # 合并 'local_date_time_full' 列
            row['local_date_time_full'] = row['local_date_time_full'][:13]
            # 求平均并更新其他列的值
            for col in df_mel_v2.columns:
                if col not in ['sort_order', 'local_date_time_full', 'name']:
                    # 如果是 str 类型，则将两个值放入一个列表中
                    if isinstance(row[col], str):
                        row[col] = [row[col], df_mel_v2.loc[idx + 1, col]]
                    # 如果是数值类型，则求平均
                    else:
                        row[col] = (row[col] + df_mel_v2.loc[idx + 1, col]) / 2
            # 将处理后的行添加到 rows_to_append 列表中
            rows_to_append.append(row)

    # 将 rows_to_append 列表中的行合并成 DataFrame，并添加到 processed_df 中
    processed_df = pd.concat([processed_df, pd.DataFrame(rows_to_append)], ignore_index=True)
    return processed_df
# 打印处理后的 DataFrame


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def merge_append(weather_data, air_data):
    weather_data['local_date_time_full'] = pd.to_datetime(weather_data['local_date_time_full'], format='%Y-%m-%d-%H').dt.strftime('%m-%d-%H')
    air_data['datetime_local'] = pd.to_datetime(air_data['datetime_local'], format='%Y-%m-%d-%H').dt.strftime('%m-%d-%H')
    merged_df = pd.merge(weather_data, air_data, left_on='local_date_time_full', right_on='datetime_local', how='inner')
    # merged_df.to_csv("data_sets/merged_data.csv", mode='a', header=False, index=False)
    print(merged_df)

#################################################################################################
# Read in static data
weather_data_static  = pd.read_csv("data_sets/weather_static.csv")
air_data_static = pd.read_csv('data_sets/air_static.csv')



# preprocess new air data and 
air_data = pd.read_csv('air_data_realtime.csv')
realtime_air_1h = find_mel_1hr_data(air_data)
# updated_air_df = concate_new_with_old(realtime_air_df, air_data_static)
# updated_air_df.to_csv('air_static.csv') 

file_path_mel = "bom_mel_realTime.json"
mel_json = read_json_file(file_path_mel)
df_mel = pd.DataFrame(mel_json)


# 新进一个air的时候， 就循环整个weather， 看下有没有对的上的
# 当时间对上了再合并存入merge的data里面， 不然的话就先放进单独的数据库等候

weather_mel_realtime = bom_first_two(df_mel)
weather_mel_realtime2 = combine_1h(weather_mel_realtime)
realtime_air_df = preprocess_new_air(realtime_air_1h)

#print(weather_mel_realtime2)
# print(realtime_air_df)

# merge_append(weather_mel_realtime2, realtime_air_df)

# realtime_air_df['datetime_local'] = pd.to_datetime(realtime_air_df['datetime_local'], format='%Y-%m-%d-%H').dt.strftime('%m-%d-%H')
# print(realtime_air_df['datetime_local']) 