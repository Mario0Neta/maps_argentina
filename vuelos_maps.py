#%%
import plotly.graph_objects as go
import pandas as pd
import airportsdata
from branca.element import Figure
import folium


vuelos_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/base_microdatos.csv")
aeropuertos_ar_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/ar-airports.csv")

# %%
vuelos_ar_df = vuelos_df[(vuelos_df["clasificacion_vuelo"] == "Cabotaje")].copy()
airports = airportsdata.load()
# %%
def get_coordinates(airports_dict: dict, type_of_coordinates:str):
    return lambda x: airports_dict.get(x, {}).get(type)

vuelos_ar_df.loc[:,"latitud_origen"] = vuelos_ar_df["origen_oaci"].map(get_coordinates(airports_dict=airports, type_of_coordinates="lat"))
vuelos_ar_df.loc[:,"longitud_origen"] = vuelos_ar_df["origen_oaci"].map(get_coordinates(airports_dict=airports, type_of_coordinates="lon"))
vuelos_ar_df.loc[:,"latitud_destino"] = vuelos_ar_df["destino_oaci"].map(get_coordinates(airports_dict=airports, type_of_coordinates="lat"))
vuelos_ar_df.loc[:,"longitud_destino"] = vuelos_ar_df["destino_oaci"].map(get_coordinates(airports_dict=airports, type_of_coordinates="lon"))
#%%
aeropuertos_df = vuelos_ar_df.drop_duplicates(subset='origen_oaci', keep='first')
#%%
vuelos_ar_df['sorted_oaci_pair'] = vuelos_ar_df.apply(
    lambda row: tuple(sorted([row['origen_oaci'], row['destino_oaci']])),
    axis=1
)
pasajeros_ar_df = vuelos_ar_df.groupby('sorted_oaci_pair').agg(
    pasajeros=('pasajeros', 'sum'),
    latitud_origen=('latitud_origen', 'first'),
    longitud_origen=('longitud_origen', 'first'),
    latitud_destino=('latitud_destino', 'first'),
    longitud_destino=('longitud_destino', "first"),
    provincia_destino=("destino_provincia", "first"),
    provincia_origen=("origen_provincia", "first")
    )
#%%
#Open street maps 
centro_argentina = [-36.616630, -64.317535]
fig = Figure(width=800, height=600)
mapa = folium.Map(location=centro_argentina, zoom_start=4)
fig.add_child(mapa)

for row in aeropuertos_df.itertuples():
    folium.CircleMarker(location=[row.latitud_origen, row.longitud_origen],
                        radius=5,
                        color="blue",
                        fill=True,
                        popup=row.origen_localidad).add_to(mapa)

total_pasajeros = pasajeros_ar_df.pasajeros.sum()

def style_function(feature):
    return {
        'color': "#FF0000",  # Initial color of the line
        'weight': max(0.5, 100*(feature['properties']['pasajeros']/total_pasajeros)),
        'opacity': 0.6
    }

def hover_style_function(feature):
    return {
        'color': "#0000FF",  # Color when hovering
        'weight': 5,
        'opacity': 0.9
    }

# Iterate over the DataFrame rows
for row in pasajeros_ar_df.itertuples():
    # Create a GeoJSON feature for each connection
    geojson_feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': [[row.longitud_origen, row.latitud_origen], [row.longitud_destino, row.latitud_destino]]
        },
        'properties': {
            'pasajeros': row.pasajeros,
            'provincia_origen': row.provincia_origen,
            'provincia_destino': row.provincia_destino
        }
    }

    # Add GeoJSON with hover effect
    folium.GeoJson(
        geojson_feature,
        style_function=style_function,
        highlight_function=hover_style_function,
        tooltip=f"Conexión entre {row.provincia_origen} y {row.provincia_destino}. {row.pasajeros} números de pasajeros"
    ).add_to(mapa)

mapa

#%%
#Plotly map
fig = go.Figure()

fig.add_trace(go.Scattergeo(
    locationmode = 'country names',
    lon = pasajeros_ar_df['longitud_origen'],
    lat = pasajeros_ar_df['latitud_origen'],
    hoverinfo = 'text',
    text = pasajeros_ar_df["provincia_origen"],
    mode = 'markers',
    marker = dict(
        size = 7,
        color = 'rgb(255, 0, 0)',
        line = dict(
            width = 30,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

flight_paths = []
for i in range(len(pasajeros_ar_df)):
    fig.add_trace(
        go.Scattergeo(
            locationmode = 'country names',
            lon = [pasajeros_ar_df['longitud_origen'][i], pasajeros_ar_df['longitud_destino'][i]],
            lat = [pasajeros_ar_df['latitud_origen'][i], pasajeros_ar_df['latitud_destino'][i]],
            mode = 'lines+markers',
            line = dict(width = 1,color = 'red'),
            opacity = float(pasajeros_ar_df['pasajeros'][i]) / float(pasajeros_ar_df['pasajeros'].max()),
        )
    ) 

fig.update_layout(
    title_text='Hover for airport names',
    showlegend=False,
    geo=dict(
        scope='south america',
        projection_type='mercator',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(0,0,0)',
    )
)

fig.write_html("maps_argentina.html")
# %%
