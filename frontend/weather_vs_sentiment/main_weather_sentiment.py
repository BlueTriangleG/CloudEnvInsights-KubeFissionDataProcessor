# Description: This script is used to run the code locally, no need to run this script in the frontend.

import weather_analysis
import seaborn as sns
import matplotlib.pyplot as plt

mastodon_file_path = '../realtimeData/output_formatted.json'
weather_file_path = '../realtimeData/weathercondition.json'

mastodon_df = weather_analysis.load_mastodon_data(mastodon_file_path)
weather_data = weather_analysis.load_weather_data(weather_file_path)

print(mastodon_df.head())

merged_df = weather_analysis.merge_weather_data(mastodon_df, weather_data)

print(merged_df.head())

print(merged_df.columns)

corr_matrix = weather_analysis.analyze_weather_impact(merged_df)
weather_analysis.visualize_weather_impact(corr_matrix)

weather_analysis.plot_scatter(merged_df, x_col='matched_air_temperature')

weather_analysis.plot_box(merged_df, x_col='matched_air_temperature')

weather_analysis.plot_time_series(merged_df, time_col='matched_datetime', y_col='sentiment')