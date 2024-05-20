import format_alignment
import sentiment_analysis
import air_quality_analysis
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 文件路径
mastodon_file_path = '../realtimeData/mastodon-aus-social.json'
air_quality_file_path = '../realtimeData/aircondition.json'
weather_file_path = '../realtimeData/weathercondition.json'

# 加载数据
mastodon_df = format_alignment.load_mastodon_data(mastodon_file_path)
air_quality_data = format_alignment.load_air_quality_data(air_quality_file_path)
weather_data = format_alignment.load_weather_data(weather_file_path)

# 合并数据
merged_df = format_alignment.merge_data(mastodon_df, air_quality_data, weather_data)

# 打印合并后的数据框，检查列名
print(merged_df.head())

# 检查合并后的数据框是否包含所需列
print(merged_df.columns)

# 添加情绪分析列
merged_df = sentiment_analysis.add_sentiment_column(merged_df)

# 分析空气质量对情绪的影响
grouped_air_quality = air_quality_analysis.analyze_air_quality_impact(merged_df)
air_quality_analysis.visualize_air_quality_impact(grouped_air_quality)

# 分析天气条件对情绪的影响
corr_matrix = air_quality_analysis.analyze_weather_impact(merged_df)
air_quality_analysis.visualize_weather_impact(corr_matrix)