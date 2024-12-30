#%%
import plotly.graph_objects as go
import pandas as pd
import airportsdata

vuelos_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/base_microdatos.csv")
aeropuertos_ar_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/ar-airports.csv")

# %%
vuelos_ar_df = vuelos_df[(vuelos_df["origen_pais"] == "Argentina") & (vuelos_df["destino_pais"] == "Argentina")].copy()
airports = airportsdata.load()
# %%
vuelos_ar_df.loc[:,"latitud_origen"] = vuelos_ar_df["origen_oaci"].map(lambda x: airports.get(x, {}).get("lat"))
vuelos_ar_df.loc[:,"longitud_origen"] = vuelos_ar_df["origen_oaci"].map(lambda x: airports.get(x, {}).get("lon"))
vuelos_ar_df.loc[:,"latitud_destino"] = vuelos_ar_df["destino_oaci"].map(lambda x: airports.get(x, {}).get("lat"))
vuelos_ar_df.loc[:,"longitud_destino"] = vuelos_ar_df["destino_oaci"].map(lambda x: airports.get(x, {}).get("lon"))
#%%
aeropuertos_df = vuelos_ar_df.drop_duplicates(subset='origen_oaci', keep='first')
aeropuertos_dict = pd.Series(
    list(zip(aeropuertos_df['latitud_origen'], aeropuertos_df['longitud_origen'], aeropuertos_df["origen_aeropuerto"])),
    index=aeropuertos_df['origen_oaci']
).to_dict()
#%%
pasajeros_ar_df = vuelos_ar_df.groupby(['origen_oaci', 'destino_oaci'])['pasajeros'].sum().reset_index()
pasajeros_ar_df['coords'] = pasajeros_ar_df['destino_oaci'].map(aeropuertos_dict)
pasajeros_ar_df['latitud_destino'] = pasajeros_ar_df['coords'].apply(lambda x: x[0] if x is not None else None)
pasajeros_ar_df['longitud_destino'] = pasajeros_ar_df['coords'].apply(lambda x: x[1] if x is not None else None)
pasajeros_ar_df['coords'] = pasajeros_ar_df['origen_oaci'].map(aeropuertos_dict)
pasajeros_ar_df['latitud_origen'] = pasajeros_ar_df['coords'].apply(lambda x: x[0] if x is not None else None)
pasajeros_ar_df['longitud_origen'] = pasajeros_ar_df['coords'].apply(lambda x: x[1] if x is not None else None)
pasajeros_ar_df["aeropuerto_origen"] = pasajeros_ar_df['coords'].apply(lambda x: x[2] if x is not None else None)

#%%
fig = go.Figure()

fig.add_trace(go.Scattergeo(
    locationmode = 'country names',
    lon = pasajeros_ar_df['longitud_origen'],
    lat = pasajeros_ar_df['latitud_origen'],
    hoverinfo = 'text',
    text = pasajeros_ar_df["aeropuerto_origen"],
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
