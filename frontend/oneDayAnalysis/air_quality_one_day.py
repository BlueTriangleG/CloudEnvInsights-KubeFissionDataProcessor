import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# load PM2.5 data
def load_pm25_data(file_path):
    with open(file_path, 'r') as f:
        pm25_data = json.load(f)
    
    records = []
    for record in pm25_data:
        source = record['_source']
        records.append({
            'datetime_local': source['datetime_local'],
            'location_name': source['location_name'],
            'BPM2_5': source['BPM2_5']
        })
    
    pm25_df = pd.DataFrame(records)
    pm25_df['datetime_local'] = pd.to_datetime(pm25_df['datetime_local'], format='%Y-%m-%d-%H')
    pm25_df.set_index('datetime_local', inplace=True)
    
    return pm25_df

# vidualize PM2.5 data
def visualize_pm25(pm25_df):
    daily_avg_pm25 = pm25_df.resample('H').mean()
    
    plt.figure(figsize=(14, 7))
    sns.lineplot(x=daily_avg_pm25.index, y=daily_avg_pm25['BPM2_5'], marker='o')
    plt.title('Daily PM2.5 Levels')
    plt.xlabel('Time')
    plt.ylabel('PM2.5')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
