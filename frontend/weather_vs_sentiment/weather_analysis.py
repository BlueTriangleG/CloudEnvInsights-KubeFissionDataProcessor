import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_weather_data(file_path):
    with open(file_path, 'r') as f:
        weather_data = json.load(f)
    
    # get the required data
    records = []
    for record in weather_data:
        source = record['_source']
        records.append({
            'datetime': source.get('local_date_time_full'),
            'location': source.get('name', 'Unknown'),
            'latitude': source.get('lat', 0.0),
            'longitude': source.get('lon', 0.0),
            'apparent_temperature': source.get('apparent_t', 0.0),
            'temperature_difference': source.get('delta_t', 0.0),
            'wind_gust_kmh': source.get('gust_kmh', 0.0),
            'wind_gust_knots': source.get('gust_kt', 0.0),
            'air_temperature': source.get('air_temp', 0.0),
            'dew_point': source.get('dewpt', 0.0),
            'pressure': source.get('press', 0.0),
            'pressure_qnh': source.get('press_qnh', 0.0),
            'pressure_msl': source.get('press_msl', 0.0),
            'relative_humidity': source.get('rel_hum', 0.0),
            'wind_speed_kmh': source.get('wind_spd_kmh', 0.0),
            'wind_speed_knots': source.get('wind_spd_kt', 0.0)
        })
    
    weather_df = pd.DataFrame(records)
    weather_df['datetime'] = pd.to_datetime(weather_df['datetime'], format='%Y-%m-%d-%H')
    
    # check the timezone information and convert if necessary
    if weather_df['datetime'].dt.tz is None:
        weather_df['datetime'] = weather_df['datetime'].dt.tz_localize('UTC')
    else:
        weather_df['datetime'] = weather_df['datetime'].dt.tz_convert('UTC')
    
    return weather_df

def load_mastodon_data(file_path):
    with open(file_path, 'r') as f:
        mastodon_data = json.load(f)
    
    # get the required data
    records = []
    for record in mastodon_data:
        source = record['_source']
        location = None
        # get the location information from tags
        for tag in source.get('tags', []):
            if tag.lower() in ['melbourne', 'sydney', 'brisbane', 'adelaide']:
                location = tag.lower().capitalize()
                break
        if not location:
            location = 'Melbourne'  # default location
        
        if location == 'Melbourne':
            location = 'Melbourne CBD'
        
        records.append({
            'post_id': source['id'],
            'created_at': source['created_at'],
            'language': source['lang'],
            'sentiment': source['sentiment'],
            'tokens': source['tokens'],
            'tags': source['tags'],
            'location': location  
        })
    
    mastodon_df = pd.DataFrame(records)
    mastodon_df['created_at'] = pd.to_datetime(mastodon_df['created_at'])
    mastodon_df['hour'] = mastodon_df['created_at'].dt.hour 
    
    # check the timezone information and convert if necessary
    if mastodon_df['created_at'].dt.tz is None:
        mastodon_df['created_at'] = mastodon_df['created_at'].dt.tz_localize('UTC')
    else:
        mastodon_df['created_at'] = mastodon_df['created_at'].dt.tz_convert('UTC')
    
    return mastodon_df



def match_data(row, data, time_col, location_col, time_window):
    matched_data = data[
        (data[time_col] <= row['created_at']) & 
        (data[time_col] >= row['created_at'] - pd.Timedelta(hours=time_window)) & 
        (data[location_col] == row['location'])
    ]
    if not matched_data.empty:
        return matched_data.iloc[0].to_dict()  
    return None

def merge_weather_data(mastodon_df, weather_data):
    matched_weather = mastodon_df.apply(lambda row: match_data(row, weather_data, 'datetime', 'location', 1), axis=1)
    matched_weather = matched_weather.dropna()
    if not matched_weather.empty:
        matched_weather_df = pd.DataFrame(matched_weather.tolist()) 
        matched_weather_df.columns = ['matched_' + str(col) for col in matched_weather_df.columns]
        merged_df = pd.concat([mastodon_df.reset_index(drop=True), matched_weather_df.reset_index(drop=True)], axis=1)
    else:
        # if no matched data found
        merged_df = mastodon_df.copy()
        for col in weather_data.columns:
            merged_df['matched_' + str(col)] = None
    return merged_df



def analyze_weather_impact(mastodon_df):
    weather_cols = ['matched_apparent_temperature', 'matched_temperature_difference', 'matched_wind_gust_kmh', 'matched_air_temperature', 'matched_dew_point', 'matched_pressure', 'matched_relative_humidity', 'matched_wind_speed_kmh']
    corr_matrix = mastodon_df[weather_cols + ['sentiment']].corr()
    return corr_matrix

def visualize_weather_impact(corr_matrix):
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', annot_kws={"size": 10})
    plt.title('Correlation Heatmap: Weather Conditions vs Sentiment', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

def plot_scatter(df, x_col, y_col='sentiment'):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_col, y=y_col, data=df)
    plt.title(f'Scatter Plot of {x_col} vs {y_col}', fontsize=16)
    plt.xlabel(x_col, fontsize=14)
    plt.ylabel(y_col, fontsize=14)
    plt.show()

def plot_box(df, x_col, y_col='sentiment'):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=df)
    plt.title(f'Box Plot of {x_col} vs {y_col}', fontsize=16)
    plt.xlabel(x_col, fontsize=14)
    plt.ylabel(y_col, fontsize=14)
    plt.show()

def plot_time_series(df, time_col, y_col):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=time_col, y=y_col, data=df)
    plt.title(f'Time Series Plot of {y_col} over {time_col}', fontsize=16)
    plt.xlabel(time_col, fontsize=14)
    plt.ylabel(y_col, fontsize=14)
    plt.show()
