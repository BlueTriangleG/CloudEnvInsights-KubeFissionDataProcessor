import pandas as pd
import json
from datetime import datetime

def load_air_quality_data(file_path):
    with open(file_path, 'r') as f:
        air_quality_data = json.load(f)
    
    # 提取需要的数据
    records = []
    for record in air_quality_data:
        source = record['_source']
        records.append({
            'datetime_local': source['datetime_local'],
            'location_name': source['location_name'],
            'BMP2_5': source['BMP2_5']
        })
    
    air_quality_df = pd.DataFrame(records)
    air_quality_df['datetime_local'] = pd.to_datetime(air_quality_df['datetime_local'], format='%Y-%m-%d-%H')
    
    # 检查时区信息并进行转换
    if air_quality_df['datetime_local'].dt.tz is None:
        air_quality_df['datetime_local'] = air_quality_df['datetime_local'].dt.tz_localize('UTC')
    else:
        air_quality_df['datetime_local'] = air_quality_df['datetime_local'].dt.tz_convert('UTC')
    
    return air_quality_df

def load_weather_data(file_path):
    with open(file_path, 'r') as f:
        weather_data = json.load(f)
    
    # 提取需要的数据
    records = []
    for record in weather_data:
        source = record['_source']
        records.append({
            'local_date_time_full': source.get('local_date_time_full'),
            'name': source.get('name', 'Unknown'),
            'lat': source.get('lat', 0.0),
            'lon': source.get('lon', 0.0),
            'apparent_t': source.get('apparent_t', 0.0),
            'delta_t': source.get('delta_t', 0.0),
            'gust_kmh': source.get('gust_kmh', 0.0),
            'gust_kt': source.get('gust_kt', 0.0),
            'air_temp': source.get('air_temp', 0.0),
            'dewpt': source.get('dewpt', 0.0),
            'press': source.get('press', 0.0),
            'press_qnh': source.get('press_qnh', 0.0),
            'press_msl': source.get('press_msl', 0.0),
            'rel_hum': source.get('rel_hum', 0.0),
            'wind_spd_kmh': source.get('wind_spd_kmh', 0.0),
            'wind_spd_kt': source.get('wind_spd_kt', 0.0)
        })
    
    weather_df = pd.DataFrame(records)
    weather_df['local_date_time_full'] = pd.to_datetime(weather_df['local_date_time_full'], format='%Y-%m-%d-%H')
    
    # 检查时区信息并进行转换
    if weather_df['local_date_time_full'].dt.tz is None:
        weather_df['local_date_time_full'] = weather_df['local_date_time_full'].dt.tz_localize('UTC')
    else:
        weather_df['local_date_time_full'] = weather_df['local_date_time_full'].dt.tz_convert('UTC')
    
    return weather_df

def load_mastodon_data(file_path):
    with open(file_path, 'r') as f:
        mastodon_data = json.load(f)
    
    # 提取需要的数据
    records = []
    for record in mastodon_data:
        source = record['_source']
        records.append({
            'id': source['id'],
            'created_at': source['created_at'],
            'lang': source['lang'],
            'sentiment': source['sentiment'],
            'tokens': source['tokens'],
            'tags': source['tags']
        })
    
    mastodon_df = pd.DataFrame(records)
    mastodon_df['created_at'] = pd.to_datetime(mastodon_df['created_at'])
    mastodon_df['hour'] = mastodon_df['created_at'].dt.hour  # 提取小时信息
    
    # 检查时区信息并进行转换
    if mastodon_df['created_at'].dt.tz is None:
        mastodon_df['created_at'] = mastodon_df['created_at'].dt.tz_localize('UTC')
    else:
        mastodon_df['created_at'] = mastodon_df['created_at'].dt.tz_convert('UTC')
    
    return mastodon_df

def match_data(row, data, time_col, time_window):
    matched_data = data[(data[time_col] <= row['created_at']) & (data[time_col] >= row['created_at'] - pd.Timedelta(hours=time_window))]
    if not matched_data.empty:
        return matched_data.iloc[0].to_dict()  # 返回字典形式
    return None

def merge_data(mastodon_df, air_quality_data, weather_data):
    matched_air_quality = mastodon_df.apply(lambda row: match_data(row, air_quality_data, 'datetime_local', 1), axis=1)
    matched_air_quality = matched_air_quality.dropna()  # 移除 None 值
    matched_air_quality_df = pd.DataFrame(matched_air_quality.tolist())  # 转换为 DataFrame
    matched_air_quality_df.columns = ['matched_' + str(col) for col in matched_air_quality_df.columns]

    matched_weather = mastodon_df.apply(lambda row: match_data(row, weather_data, 'local_date_time_full', 1), axis=1)
    matched_weather = matched_weather.dropna()  # 移除 None 值
    matched_weather_df = pd.DataFrame(matched_weather.tolist())  # 转换为 DataFrame
    matched_weather_df.columns = ['matched_' + str(col) for col in matched_weather_df.columns]

    merged_df = pd.concat([mastodon_df.reset_index(drop=True), matched_air_quality_df.reset_index(drop=True), matched_weather_df.reset_index(drop=True)], axis=1)
    return merged_df
