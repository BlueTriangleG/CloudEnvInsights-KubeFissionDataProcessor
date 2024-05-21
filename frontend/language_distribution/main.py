# Description: This script is used to run the code locally, no need to run this script in the frontend.

import pandas as pd
import language_analysis

mastodon_file_path = '../realtimeData/output_formatted.json'
mastodon_df = language_analysis.load_mastodon_data(mastodon_file_path)

location_language_distribution = language_analysis.analyze_language_distribution_by_location(mastodon_df)

print(location_language_distribution)

language_analysis.visualize_language_distribution_by_location(location_language_distribution)
