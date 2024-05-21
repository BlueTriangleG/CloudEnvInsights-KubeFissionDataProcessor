import pandas as pd
import json

def load_air_quality_data(file_path):
    with open(file_path, 'r') as f:
        air_quality_data = json.load(f)
    
    # get the required data
    records = []
    for record in air_quality_data:
        source = record['_source']
        records.append({
            'datetime_local': source['datetime_local'],
            'location_name': source['location_name'],
            'BPM2_5': source['BPM2_5']
        })
    
    air_quality_df = pd.DataFrame(records)
    air_quality_df['datetime_local'] = pd.to_datetime(air_quality_df['datetime_local'], format='%Y-%m-%d-%H')
    
    # check the timezone information and convert if necessary
    if air_quality_df['datetime_local'].dt.tz is None:
        air_quality_df['datetime_local'] = air_quality_df['datetime_local'].dt.tz_localize('UTC')
    else:
        air_quality_df['datetime_local'] = air_quality_df['datetime_local'].dt.tz_convert('UTC')
    
    return air_quality_df

def load_mastodon_data(file_path):
    with open(file_path, 'r') as f:
        mastodon_data = json.load(f)
    
    records = []
    for record in mastodon_data:
        source = record['_source']
        location = None
        for tag in source.get('tags', []):
            if tag.lower() in ['melbourne', 'sydney', 'brisbane', 'adelaide']:  # can add more cities
                location = tag.lower().capitalize()
                break
        if not location:
            location = 'Around Australia'  

        records.append({
            'id': source['id'],
            'created_at': source['created_at'],
            'lang': source['lang'],
            'sentiment': source['sentiment'],
            'tokens': source['tokens'],
            'tags': source['tags'],
            'location': location
        })
    
    mastodon_df = pd.DataFrame(records)
    mastodon_df['created_at'] = pd.to_datetime(mastodon_df['created_at'])
    mastodon_df['hour'] = mastodon_df['created_at'].dt.hour  # get the hour of the day
    
    # check the timezone information and convert if necessary
    if mastodon_df['created_at'].dt.tz is None:
        mastodon_df['created_at'] = mastodon_df['created_at'].dt.tz_localize('UTC')
    else:
        mastodon_df['created_at'] = mastodon_df['created_at'].dt.tz_convert('UTC')
    
    return mastodon_df

def match_air_quality(row, air_quality_data):
    matched_data = air_quality_data[(air_quality_data['location_name'] == row['location']) & 
                                    (air_quality_data['datetime_local'] <= row['created_at']) & 
                                    (air_quality_data['datetime_local'] >= row['created_at'] - pd.Timedelta(hours=1))]
    if not matched_data.empty:
        return matched_data.iloc[0].to_dict() 
    return None

def merge_data(mastodon_df, air_quality_data):
    matched_air_quality = mastodon_df.apply(lambda row: match_air_quality(row, air_quality_data), axis=1)
    matched_air_quality = matched_air_quality.dropna()  
    matched_air_quality_df = pd.DataFrame(matched_air_quality.tolist()) 
    # rename the columns
    matched_air_quality_df.columns = ['matched_' + str(col) for col in matched_air_quality_df.columns]
    merged_df = pd.concat([mastodon_df.reset_index(drop=True), matched_air_quality_df.reset_index(drop=True)], axis=1)
    return merged_df
