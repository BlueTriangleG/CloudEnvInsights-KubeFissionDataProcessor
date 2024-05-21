import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import json

def json_to_dataframe(json_file_path):
    """
    Read a JSON file and convert it to a DataFrame.
    
    Parameters:
    json_file_path (str): Path to the JSON file.

    Returns:
    pd.DataFrame: DataFrame containing JSON data.
    """
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Extract the _source field data
    source_data = [item['_source'] for item in json_data]

    # Create DataFrame
    df = pd.DataFrame(source_data)

    return df

def preprocess(df):
    """
    Preprocess the DataFrame by dropping specific columns and handling missing values.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: Cleaned DataFrame.
    """
    columns_to_drop = ['Unnamed: 0.2', 'name', 'Unnamed: 0.3']
    df2 = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
    df_cleaned_columns = df2.dropna()
    return df_cleaned_columns

# Paths to JSON files
weather_path = '../realtimeData/weathercondition.json'
air_path = '../realtimeData/aircondition_data2.json'

# Convert JSON files to DataFrames
weather_data = json_to_dataframe(weather_path)
air_data = json_to_dataframe(air_path)

# Convert datetime columns to common format
weather_data['local_date_time_full'] = pd.to_datetime(weather_data['local_date_time_full'], format='%Y-%m-%d-%H').dt.strftime('%m-%d-%H')
air_data['datetime_local'] = pd.to_datetime(air_data['datetime_local'], format='%Y-%m-%d-%H').dt.strftime('%m-%d-%H')

# Merge DataFrames on the datetime columns
merged_df = pd.merge(weather_data, air_data, left_on='local_date_time_full', right_on='datetime_local', how='inner')

# Drop unnecessary columns
merged_df.drop(columns=['location_name', 'vis_km', 'rain_trace', 'datetime_local'], inplace=True)
merged_df.dropna()
merged_df['name'] = 'Melbourne'

# Clean the merged DataFrame
df_cleaned = preprocess(merged_df)

# Convert datetime column back to datetime format
df_cleaned['local_date_time_full'] = pd.to_datetime(df_cleaned['local_date_time_full'], format='%m-%d-%H')

# Extract date and month-day information for plotting
df_cleaned['date'] = df_cleaned['local_date_time_full'].dt.date
df_cleaned['month_day'] = df_cleaned['local_date_time_full'].dt.strftime('%b-%d')

# Plot PM2.5 over time by date with months displayed on x-axis
plt.figure(figsize=(12, 6))
sns.lineplot(x='date', y='BMP2_5', data=df_cleaned, marker='o')
plt.xticks(ticks=df_cleaned['date'], labels=df_cleaned['month_day'], rotation=45)
plt.title('PM2.5 Over Time by Date (Months Displayed)')
plt.xlabel('Month-Day')
plt.ylabel('BMP2_5')
plt.show()

# Filter DataFrame to keep only relevant columns for analysis
columns_to_keep = ['apparent_t', 'delta_t', 'gust_kmh', 'gust_kt', 'air_temp', 'dewpt', 'press', 'press_qnh', 'press_msl', 'rel_hum', 'wind_spd_kmh', 'wind_spd_kt', 'BMP2_5']
filtered_df = df_cleaned[columns_to_keep]

# Plot the correlation matrix
plt.figure(figsize=(12, 8))
corr_matrix = filtered_df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()

# Prepare data for model training
X = df_cleaned.drop(columns=['BMP2_5', 'local_date_time_full', 'date', 'month_day','wind_dir'])   # Feature variables
y = df_cleaned['BMP2_5']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate and print evaluation metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
