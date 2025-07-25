import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium
from folium.plugins import MarkerCluster

# Read data
df = pd.read_csv("US_Accidents_March23.csv", nrows=100000)

# Clean data
df.drop(['End_Lat', 'End_Lng', 'Wind_Chill(F)', 'Precipitation(in)'], axis=1, inplace=True)
df.dropna(inplace=True)

# Convert Start_Time to datetime and extract features
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
df['Hour'] = df['Start_Time'].dt.hour
df['Day'] = df['Start_Time'].dt.day_name()
df['Month'] = df['Start_Time'].dt.month_name()

# 1. Accidents by Hour (Line Plot with Area)
hour_counts = df['Hour'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x=hour_counts.index, y=hour_counts.values, color='purple', linewidth=3, marker='o')
plt.fill_between(hour_counts.index, hour_counts.values, color='purple', alpha=0.2)
plt.title('Accidents by Hour of Day', fontsize=14)
plt.xlabel('Hour of Day')
plt.ylabel('Number of Accidents')
plt.xticks(range(0, 24))
plt.show()

# 2. Accidents by Day (Horizontal Bar Chart with Gradient)
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_counts = df['Day'].value_counts()[day_order]

colors = sns.color_palette("coolwarm", len(day_counts))
plt.figure(figsize=(10, 6))
plt.barh(day_counts.index, day_counts.values, color=colors)
plt.title('Accidents by Day of Week', fontsize=14)
plt.xlabel('Number of Accidents')
plt.ylabel('Day of Week')
for i, v in enumerate(day_counts.values):
    plt.text(v+500, i, str(v), va='center')
plt.show()

#  3. Accidents by Month (Radar Chart)
month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
month_counts = df['Month'].value_counts()[month_order]

# Radar setup
angles = np.linspace(0, 2*np.pi, len(month_order), endpoint=False).tolist()
month_counts_values = month_counts.values.tolist()
month_counts_values += month_counts_values[:1]  # repeat first value to close the circle
angles += angles[:1]

fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
ax.plot(angles, month_counts_values, color='orange', linewidth=2)
ax.fill(angles, month_counts_values, color='orange', alpha=0.25)
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(month_order, fontsize=10)
ax.tick_params(pad=15)
plt.title('Accidents by Month', fontsize=14, y=1.1)
plt.show()



# Center of the map (mean coordinates)
map_center = [df['Start_Lat'].mean(), df['Start_Lng'].mean()]
m = folium.Map(location=map_center, zoom_start=6)

marker_cluster = MarkerCluster().add_to(m)

for idx, row in df.sample(5000).iterrows():  # sampling for performance
    folium.Marker(location=[row['Start_Lat'], row['Start_Lng']]).add_to(marker_cluster)

m.save('accident_hotspots_map.html')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# List of road condition features (booleans)
road_conditions = [
    'Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit',
    'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming',
    'Traffic_Signal', 'Turning_Loop'
]

# Calculate number of accidents for each condition (True means condition present)
condition_counts = df[road_conditions].sum().sort_values(ascending=False)

# Plot horizontal bar chart
colors = sns.color_palette("viridis", len(condition_counts))
plt.figure(figsize=(12, 6))
sns.barplot(x=condition_counts.values, y=condition_counts.index, color=None)  # No palette
bars = plt.barh(condition_counts.index, condition_counts.values, color=colors)

plt.title('Number of Accidents by Road Condition Features')
plt.xlabel('Number of Accidents')
plt.ylabel('Road Condition Feature')

# Add counts
for i, v in enumerate(condition_counts.values):
    plt.text(v + 50, i, str(v), va='center')

plt.show()

import pandas as pd
import plotly.express as px

# Count accidents by weather condition
weather_counts = df['Weather_Condition'].value_counts().head(15)  # Top 15 conditions

# Create interactive bar chart
fig = px.bar(
    x=weather_counts.values,
    y=weather_counts.index,
    orientation='h',
    title='Accidents by Weather Condition',
    labels={'x': 'Number of Accidents', 'y': 'Weather Condition'},
    color=weather_counts.values,  # Gradient color by count
    color_continuous_scale='viridis'
)

fig.update_layout(
    template='plotly_dark',  # Dark dashboard theme
    title_font_size=20,
    xaxis_title='Number of Accidents',
    yaxis_title='Weather Condition',
    width=900,
    height=600
)

fig.show()
