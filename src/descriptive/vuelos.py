# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import airportsdata

vuelos_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/base_microdatos.csv")
aeropuertos_ar_df = pd.read_csv(
    "/home/leontxo/Documents/maps_argentina/ar-airports.csv"
)

# %%
vuelos_ar_df = vuelos_df[
    (vuelos_df["origen_pais"] == "Argentina")
    & (vuelos_df["destino_pais"] == "Argentina")
].copy()
airports = airportsdata.load()
# %%
vuelos_ar_df.loc[:, "latitud_origen"] = vuelos_ar_df["origen_oaci"].map(
    lambda x: airports.get(x, {}).get("lat")
)
vuelos_ar_df.loc[:, "longitud_origen"] = vuelos_ar_df["origen_oaci"].map(
    lambda x: airports.get(x, {}).get("lon")
)
vuelos_ar_df.loc[:, "latitud_destino"] = vuelos_ar_df["destino_oaci"].map(
    lambda x: airports.get(x, {}).get("lat")
)
vuelos_ar_df.loc[:, "longitud_destino"] = vuelos_ar_df["destino_oaci"].map(
    lambda x: airports.get(x, {}).get("lon")
)

# %%
fig = go.Figure()
fig.add_trace(
    go.Scattergeo(
        locationmode="USA-states",
        lon=vuelos_ar_df["longitud_origen"],
        lat=vuelos_ar_df["latitud_origen"],
        hoverinfo="text",
        text=vuelos_ar_df["origen_aeropuerto"],
        mode="markers",
        marker=dict(
            size=2,
            color="rgb(255, 0, 0)",
            line=dict(width=3, color="rgba(68, 68, 68, 0)"),
        ),
    )
)
# %%
