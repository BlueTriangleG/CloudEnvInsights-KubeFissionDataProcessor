import format_alignment
import sentiment_analysis
import air_quality_analysis
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 文件路径
mastodon_file_path = '../realtimeData/output_formatted.json'
air_quality_file_path = '../realtimeData/aircondition.json'

# 加载数据
mastodon_df = format_alignment.load_mastodon_data(mastodon_file_path)
air_quality_data = format_alignment.load_air_quality_data(air_quality_file_path)

# 合并数据
merged_df = format_alignment.merge_data(mastodon_df, air_quality_data)

# 添加情绪分析列
merged_df = sentiment_analysis.add_sentiment_column(merged_df)

# 分析空气质量对情绪的影响
grouped = air_quality_analysis.analyze_air_quality_impact(merged_df)

# 可视化结果
air_quality_analysis.visualize_air_quality_impact(grouped)

# 相关图
def plot_correlation(df):
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.show()

# 散点图
def plot_scatter(df):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='matched_BMP2_5', y='sentiment', data=df)
    plt.title('Scatter Plot of Sentiment vs Air Quality (PM2.5)')
    plt.xlabel('PM2.5')
    plt.ylabel('Sentiment')
    plt.show()

# 热图
def plot_heatmap(df):
    heatmap_data = df.pivot_table(index='hour', columns='air_quality_category', values='sentiment', aggfunc='mean')
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='.2f')
    plt.title('Heatmap of Sentiment by Hour and Air Quality Category')
    plt.xlabel('Air Quality Category')
    plt.ylabel('Hour')
    plt.show()

# 创建图表
plot_correlation(merged_df)
plot_scatter(merged_df)
plot_heatmap(merged_df)
