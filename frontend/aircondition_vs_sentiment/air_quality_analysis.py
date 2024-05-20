import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def categorize_air_quality(bmp2_5_value):
    if bmp2_5_value <= 12:
        return 'Good'
    elif bmp2_5_value <= 35.4:
        return 'Moderate'
    elif bmp2_5_value <= 55.4:
        return 'Unhealthy for Sensitive Groups'
    elif bmp2_5_value <= 150.4:
        return 'Unhealthy'
    elif bmp2_5_value <= 250.4:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'

def analyze_air_quality_impact(mastodon_df):
    # 使用新的列名
    mastodon_df['air_quality_category'] = mastodon_df['matched_BMP2_5'].apply(categorize_air_quality)
    grouped = mastodon_df.groupby('air_quality_category').agg({'sentiment': 'mean'}).reset_index()
    grouped.columns = ['Air Quality Category', 'Average Sentiment']
    return grouped

def analyze_weather_impact(mastodon_df):
    weather_cols = ['matched_apparent_t', 'matched_delta_t', 'matched_gust_kmh', 'matched_air_temp', 'matched_dewpt', 'matched_press', 'matched_rel_hum', 'matched_wind_spd_kmh']
    corr_matrix = mastodon_df[weather_cols + ['sentiment']].corr()
    return corr_matrix

def visualize_air_quality_impact(grouped):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Air Quality Category', y='Average Sentiment', data=grouped, palette="coolwarm")
    plt.title('Average Sentiment by Air Quality Category')
    plt.xlabel('Air Quality Category')
    plt.ylabel('Average Sentiment')
    plt.show()

def visualize_weather_impact(corr_matrix):
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap: Weather Conditions vs Sentiment')
    plt.show()
