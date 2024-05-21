import pandas as pd
import language_analysis

# 加载 Mastodon 数据
mastodon_file_path = '../realtimeData/output_formatted.json'
mastodon_df = language_analysis.load_mastodon_data(mastodon_file_path)

# 按地区分析语言分布
location_language_distribution = language_analysis.analyze_language_distribution_by_location(mastodon_df)

# 打印结果
print(location_language_distribution)

# 可视化结果
language_analysis.visualize_language_distribution_by_location(location_language_distribution)
