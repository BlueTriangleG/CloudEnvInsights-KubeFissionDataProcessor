import folium
from folium import plugins
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import json

def load_data_from_json(file_path):
    """
    Load data from a JSON file into a pandas DataFrame.

    Args:
    file_path (str): Path to the JSON file.

    Returns:
    pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None



def plot_geospatial_data_folium(df, lon_col, lat_col, size_col, color_col, title, cmap='YlOrRd'):
    """
    Plot geospatial data on an interactive map using folium.

    Args:
    df (pd.DataFrame): DataFrame containing geospatial data.
    lon_col (str): Column name for longitude data.
    lat_col (str): Column name for latitude data.
    size_col (str): Column name for data used to size the plot markers.
    color_col (str): Column name for data used to color the plot markers.
    title (str): Title of the plot.
    cmap (str): Colormap for the plot markers.

    Returns:
    folium.Map: Interactive map with plotted data.
    """
    # Debugging: Print column names
    print("DataFrame columns:", df.columns)
    
    # Check if all required columns are in the DataFrame
    required_columns = [lon_col, lat_col, size_col, color_col]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Column '{col}' not found in DataFrame")
    
    # Initialize the map at an average location
    map_center = [df[lat_col].mean(), df[lon_col].mean()]
    folium_map = folium.Map(location=map_center, zoom_start=10, tiles='OpenStreetMap')

    # Normalize color column to fit color map
    norm = matplotlib.colors.Normalize(vmin=df[color_col].min(), vmax=df[color_col].max())
    cmap = plt.cm.get_cmap(cmap)

    # Add points to the map
    for _, row in df.iterrows():
        color = matplotlib.colors.to_hex(cmap(norm(row[color_col])))
        popup_text = (f"Legal Name: {row['legal_name']}<br>"
                      f"Suburb: {row['suburb']}<br>"
                      f"Address: {row['address']}<br>"
                      f"Avg Air Quality: {row[color_col]}")
        folium.CircleMarker(
            location=(row[lat_col], row[lon_col]),
            radius=row[size_col] / 100,  # Adjust size to fit map scale
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(folium_map)
    
    # Add title
    title_html = f'''
        <h3 align="center" style="font-size:20px"><b>{title}</b></h3>
        '''
    folium_map.get_root().html.add_child(folium.Element(title_html))

    return folium_map