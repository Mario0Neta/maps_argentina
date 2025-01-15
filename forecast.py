#%%
import matplotlib.pyplot as plt
import pandas as pd

vuelos_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/base_microdatos.csv")
vuelos_ar_df = vuelos_df[(vuelos_df["clasificacion_vuelo"] == "Cabotaje")].copy()
vuelos_ar_df["fecha"] = pd.to_datetime(vuelos_ar_df['indice_tiempo'])
vuelos_ar_df = vuelos_ar_df
# %%
