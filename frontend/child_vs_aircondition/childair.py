import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from sklearn.cluster import KMeans

# 读取 child-air-quality.json 文件
with open('child-air-quality.json', 'r') as file:
    data = json.load(file)

# 提取每个记录的 "_source" 字段中的内容
extracted_data = [item['_source'] for item in data]

# 将提取的数据写入 child_care_with_air_quality.json 文件
with open('child_care_with_air_quality.json', 'w') as file:
    json.dump(extracted_data, file, indent=4)

print("数据已转换并保存为 child_care_with_air_quality.json")

# 读取 child_care_with_air_quality.json 文件
with open('./child_care_with_air_quality.json', 'r') as f:
    air_data = json.load(f)

# 创建 DataFrame
airdf = pd.DataFrame(air_data)

# Basic statistics
df = airdf
print(df.describe())

# Unique values in categorical columns
print(df['suburb'].unique())

# Distribution of numerical data
plt.figure(figsize=(10, 6))
sns.histplot(df['avg_air_quality'], bins=30, kde=True)
plt.title('Distribution of Average Air Quality')
plt.xlabel('Average Air Quality')
plt.ylabel('Frequency')
plt.savefig('avg_air_quality_distribution.png')
plt.show()
plt.close()

# Scatter plot with color bar
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(data=df, x='longitude', y='latitude', hue='avg_air_quality', palette='viridis')
plt.title('Air Quality by Location')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.colorbar(scatter.collections[0], label='Average Air Quality')
plt.savefig('air_quality_by_location.png')
plt.show()
plt.close()

plt.figure(figsize=(12, 8))
sns.barplot(data=df, x='suburb', y='avg_air_quality', palette='viridis')
plt.title('Average Air Quality by Suburb')
plt.xlabel('Suburb')
plt.ylabel('Average Air Quality')
plt.xticks(rotation=90)
plt.savefig('avg_air_quality_by_suburb.png')
plt.show()
plt.close()

# Group by suburb and calculate the mean air quality
suburb_avg_air_quality = df.groupby('suburb')['avg_air_quality'].mean().reset_index()

# Select the top 10 suburbs with the highest average air quality
top_suburbs = suburb_avg_air_quality.nlargest(10, 'avg_air_quality')

# Bar plot
plt.figure(figsize=(12, 8))
sns.barplot(data=top_suburbs, x='suburb', y='avg_air_quality', palette='viridis')
plt.title('Top 10 Suburbs by Average Air Quality')
plt.xlabel('Suburb')
plt.ylabel('Average Air Quality')
plt.xticks(rotation=90)
plt.savefig('top_10_suburbs_air_quality.png')
plt.show()
plt.close()

# Create a map centered around the average latitude and longitude
map_center = [df['latitude'].mean(), df['longitude'].mean()]
map_ = folium.Map(location=map_center, zoom_start=12)

# Add markers to the map
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        popup=f"{row['legal_name']} - {row['avg_air_quality']}",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(map_)

# Save the map to an HTML file
map_.save('air_quality_map.html')

# Select features for clustering
X = df[['longitude', 'latitude', 'avg_air_quality']]

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3)
df['cluster'] = kmeans.fit_predict(X)

# Visualize clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='longitude', y='latitude', hue='cluster', palette='viridis')
plt.title('Clusters of Air Quality')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('air_quality_clusters.png')



