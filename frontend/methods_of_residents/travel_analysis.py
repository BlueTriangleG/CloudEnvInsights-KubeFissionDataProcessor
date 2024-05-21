import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns

# define travel modes and their keywords
travel_modes = {
    'car': ['car', 'automobile', 'vehicle'],
    'bus': ['bus', 'coach'],
    'bike': ['bike', 'bicycle', 'cycling'],
    'walk': ['walk', 'walking', 'foot'],
    'train': ['train', 'railway', 'subway'],
    'scooter': ['scooter', 'e-scooter']
}

def load_mastodon_data(file_path):
    with open(file_path, 'r') as f:
        mastodon_data = json.load(f)
    
    records = []
    for record in mastodon_data:
        source = record['_source']
        location = None
        for tag in source.get('tags', []):
            if tag.lower() in ['melbourne', 'sydney', 'brisbane', 'adelaide']: 
                location = tag.lower().capitalize()
                break
        if not location:
            location = 'Around Australia'
        
        records.append({
            'post_id': source['id'],
            'created_at': source['created_at'],
            'tokens': source['tokens'],  
            'tags': source['tags'],
            'location': location
        })
    
    mastodon_df = pd.DataFrame(records)
    mastodon_df['created_at'] = pd.to_datetime(mastodon_df['created_at'])
    
    if mastodon_df['created_at'].dt.tz is None:
        mastodon_df['created_at'] = mastodon_df['created_at'].dt.tz_localize('UTC')
    else:
        mastodon_df['created_at'].dt.tz_convert('UTC')
    
    return mastodon_df

def extract_travel_modes(tokens):
    modes = []
    for mode, keywords in travel_modes.items():
        for token in tokens:
            if token.lower() in keywords:
                modes.append(mode)
                break
    return modes

def analyze_travel_modes(mastodon_df):
    # extract travel modes from tokens
    mastodon_df['travel_modes'] = mastodon_df['tokens'].apply(extract_travel_modes)
    mastodon_df = mastodon_df.explode('travel_modes')
    
    # count the occurrences of each travel mode
    travel_stats = mastodon_df.groupby(['location', 'travel_modes']).size().reset_index(name='counts')
    
    # find the most popular travel mode in each location
    most_popular_travel_modes = travel_stats.loc[travel_stats.groupby('location')['counts'].idxmax()]
    
    return travel_stats, most_popular_travel_modes

def visualize_travel_modes_by_city(travel_stats):
    locations = travel_stats['location'].unique()
    
    for location in locations:
        location_stats = travel_stats[travel_stats['location'] == location]
        plt.figure(figsize=(12, 6))
        sns.barplot(x='travel_modes', y='counts', data=location_stats)
        plt.title(f'Most Popular Travel Modes in {location}', fontsize=16)
        plt.xlabel('Travel Modes', fontsize=14)
        plt.ylabel('Counts', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.tight_layout()
        plt.show()