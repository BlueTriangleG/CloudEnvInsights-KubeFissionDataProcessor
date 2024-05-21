import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

# map language code to full name
LANGUAGE_MAP = {
    'en': 'English',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'it': 'Italian',
    'pt': 'Portuguese',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ru': 'Russian',
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
            'language': source['lang'],  
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

def analyze_language_distribution_by_location(mastodon_df):
    # calculate the distribution of languages in each location
    location_language_distribution = mastodon_df.groupby(['location', 'language']).size().reset_index(name='counts')
    
    # keep the top 10 languages for each location
    top_languages_by_location = location_language_distribution.groupby('location').apply(
        lambda x: x.nlargest(10, 'counts')
    ).reset_index(drop=True)
    
    # add full language name
    top_languages_by_location['language_full'] = top_languages_by_location['language'].map(LANGUAGE_MAP)
    
    return top_languages_by_location

def visualize_language_distribution_by_location(location_language_distribution):
    # draw bar plots for each location
    locations = location_language_distribution['location'].unique()
    
    for location in locations:
        plt.figure(figsize=(12, 8))
        data = location_language_distribution[location_language_distribution['location'] == location]
        sns.barplot(x='language_full', y='counts', data=data)
        plt.title(f'Language Distribution in {location}', fontsize=16)
        plt.xlabel('Language', fontsize=14)
        plt.ylabel('Counts', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.show()
