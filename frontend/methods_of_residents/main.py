# Description: This script is used to run the code locally, no need to run this script in the frontend.

import pandas as pd
import travel_analysis

mastodon_file_path = '../realtimeData/mastodon-aus-social.json'
mastodon_df = travel_analysis.load_mastodon_data(mastodon_file_path)

travel_stats, most_popular_travel_modes = travel_analysis.analyze_travel_modes(mastodon_df)

print(travel_stats)
print(most_popular_travel_modes)

travel_analysis.visualize_travel_modes_by_city(travel_stats)
