import weather_analysis
import seaborn as sns
import matplotlib.pyplot as plt

# 文件路径
mastodon_file_path = '../realtimeData/output_formatted.json'
weather_file_path = '../realtimeData/weathercondition.json'

# 加载数据
mastodon_df = weather_analysis.load_mastodon_data(mastodon_file_path)
weather_data = weather_analysis.load_weather_data(weather_file_path)

# 打印加载的数据，检查地理位置信息
print(mastodon_df.head())

# 合并数据
merged_df = weather_analysis.merge_weather_data(mastodon_df, weather_data)

# 打印合并后的数据框，检查列名
print(merged_df.head())

# 检查合并后的数据框是否包含所需列
print(merged_df.columns)

# 分析天气条件对情绪的影响
corr_matrix = weather_analysis.analyze_weather_impact(merged_df)
weather_analysis.visualize_weather_impact(corr_matrix)

# 散点图示例
weather_analysis.plot_scatter(merged_df, x_col='matched_air_temperature')

# 箱线图示例
weather_analysis.plot_box(merged_df, x_col='matched_air_temperature')

# 时间序列图示例
weather_analysis.plot_time_series(merged_df, time_col='matched_datetime', y_col='sentiment')