import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# 加载天气数据
def load_weather_data(file_path):
    with open(file_path, 'r') as f:
        weather_data = json.load(f)
    
    # 提取需要的数据
    records = []
    for record in weather_data:
        source = record['_source']
        records.append({
            'datetime_local': source['local_date_time_full'],
            'location_name': source['name'],
            'apparent_t': source['apparent_t'],
            'air_temp': source['air_temp'],
            'rel_hum': source['rel_hum'],
            'press': source['press'],
            'wind_spd_kmh': source['wind_spd_kmh']
        })
    
    weather_df = pd.DataFrame(records)
    weather_df['datetime_local'] = pd.to_datetime(weather_df['datetime_local'], format='%Y-%m-%d-%H')
    weather_df.set_index('datetime_local', inplace=True)
    
    return weather_df

# 可视化天气数据
def visualize_weather_data(weather_df):
    plt.figure(figsize=(14, 10))
    
    # 绘制气温变化
    plt.subplot(3, 1, 1)
    sns.lineplot(data=weather_df, x=weather_df.index, y='air_temp', marker='o', label='Air Temp (°C)')
    sns.lineplot(data=weather_df, x=weather_df.index, y='apparent_t', marker='o', label='Apparent Temp (°C)')
    plt.title('Temperature Over Time')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)
    
    # 绘制相对湿度变化
    plt.subplot(3, 1, 2)
    sns.lineplot(data=weather_df, x=weather_df.index, y='rel_hum', marker='o', color='b')
    plt.title('Relative Humidity Over Time')
    plt.xlabel('Time')
    plt.ylabel('Relative Humidity (%)')
    plt.grid(True)
    
    # 绘制风速变化
    plt.subplot(3, 1, 3)
    sns.lineplot(data=weather_df, x=weather_df.index, y='wind_spd_kmh', marker='o', color='g')
    plt.title('Wind Speed Over Time')
    plt.xlabel('Time')
    plt.ylabel('Wind Speed (km/h)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

