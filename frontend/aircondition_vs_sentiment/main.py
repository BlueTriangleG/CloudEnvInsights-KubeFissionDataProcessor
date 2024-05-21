# Description: This script is used to run the code locally, no need to run this script in the frontend.

import format_alignment
import sentiment_analysis
import air_quality_analysis
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# file paths
mastodon_file_path = '../realtimeData/mastodon-aus-social.json'
air_quality_file_path = '../realtimeData/aircondition.json'

# load data
mastodon_df = format_alignment.load_mastodon_data(mastodon_file_path)
air_quality_data = format_alignment.load_air_quality_data(air_quality_file_path)

# combine data
merged_df = format_alignment.merge_data(mastodon_df, air_quality_data)

# add sentiment column
merged_df = sentiment_analysis.add_sentiment_column(merged_df)

grouped = air_quality_analysis.analyze_air_quality_impact(merged_df)

air_quality_analysis.visualize_air_quality_impact(grouped)

def plot_correlation(df):
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.show()

def plot_scatter(df):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='matched_BMP2_5', y='sentiment', data=df)
    plt.title('Scatter Plot of Sentiment vs Air Quality (PM2.5)')
    plt.xlabel('PM2.5')
    plt.ylabel('Sentiment')
    plt.show()

def plot_heatmap(df):
    heatmap_data = df.pivot_table(index='hour', columns='air_quality_category', values='sentiment', aggfunc='mean')
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='.2f')
    plt.title('Heatmap of Sentiment by Hour and Air Quality Category')
    plt.xlabel('Air Quality Category')
    plt.ylabel('Hour')
    plt.show()

plot_correlation(merged_df)
plot_scatter(merged_df)
plot_heatmap(merged_df)