import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# 加载 PM2.5 数据
def load_pm25_data(file_path):
    with open(file_path, 'r') as f:
        pm25_data = json.load(f)
    
    # 提取需要的数据
    records = []
    for record in pm25_data:
        source = record['_source']
        records.append({
            'datetime_local': source['datetime_local'],
            'location_name': source['location_name'],
            'BMP2_5': source['BMP2_5']
        })
    
    pm25_df = pd.DataFrame(records)
    pm25_df['datetime_local'] = pd.to_datetime(pm25_df['datetime_local'], format='%Y-%m-%d-%H')
    pm25_df.set_index('datetime_local', inplace=True)
    
    return pm25_df

# 可视化 PM2.5 数据
def visualize_pm25(pm25_df):
    # 按天和小时进行平均
    daily_avg_pm25 = pm25_df.resample('H').mean()
    
    plt.figure(figsize=(14, 7))
    sns.lineplot(x=daily_avg_pm25.index, y=daily_avg_pm25['BMP2_5'], marker='o')
    plt.title('Daily PM2.5 Levels')
    plt.xlabel('Time')
    plt.ylabel('PM2.5')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
