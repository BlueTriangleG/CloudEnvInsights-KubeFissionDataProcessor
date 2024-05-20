import pandas as pd
import travel_analysis

# 加载 Mastodon 数据
mastodon_file_path = '../realtimeData/output_formatted.json'
mastodon_df = travel_analysis.load_mastodon_data(mastodon_file_path)

# 分析出行方式
travel_stats, most_popular_travel_modes = travel_analysis.analyze_travel_modes(mastodon_df)

# 打印结果
print(travel_stats)
print(most_popular_travel_modes)

# 可视化结果
travel_analysis.visualize_travel_modes(travel_stats)
