import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def categorize_air_quality(bmp2_5_value):
    if pd.isna(bmp2_5_value):
        return 'No Data'
    if bmp2_5_value <= 5:
        return 'Good'
    elif bmp2_5_value <= 12:
        return 'Moderate'
    elif bmp2_5_value <= 35:
        return 'Unhealthy for Sensitive Groups'
    elif bmp2_5_value <= 55:
        return 'Unhealthy'
    elif bmp2_5_value <= 150:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'

def analyze_air_quality_impact(mastodon_df):
    mastodon_df['air_quality_category'] = mastodon_df['matched_BPM2_5'].apply(categorize_air_quality)
    grouped = mastodon_df.groupby('air_quality_category').agg({'sentiment': 'mean'}).reset_index()
    grouped.columns = ['Air Quality Category', 'Average Sentiment']
    return grouped

def visualize_air_quality_impact(grouped):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Air Quality Category', y='Average Sentiment', data=grouped, palette="coolwarm")
    plt.title('Average Sentiment by Air Quality Category')
    plt.xlabel('Air Quality Category')
    plt.ylabel('Average Sentiment')
    plt.show()

def plot_scatter(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='matched_BPM2_5', y='sentiment', data=df, hue='air_quality_category', palette='coolwarm', alpha=0.6)
    plt.title('Sentiment vs Air Quality (BPM2_5)')
    plt.xlabel('BPM2_5')
    plt.ylabel('Sentiment')
    plt.legend(title='Air Quality Category')
    plt.show()

def plot_heatmap(df):
    heatmap_data = df.pivot_table(index='hour', columns='air_quality_category', values='sentiment', aggfunc='mean')
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='.2f')
    plt.title('Heatmap of Sentiment by Hour and Air Quality Category')
    plt.xlabel('Air Quality Category')
    plt.ylabel('Hour')
    plt.show()