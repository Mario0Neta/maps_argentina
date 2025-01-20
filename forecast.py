#%%
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

vuelos_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/base_microdatos.csv")
vuelos_ar_df = vuelos_df[(vuelos_df["clasificacion_vuelo"] == "Cabotaje")].copy()
vuelos_cordoba_df = vuelos_ar_df[(vuelos_ar_df["origen_provincia"] == "Córdoba") | (vuelos_ar_df["destino_provincia"] == "Córdoba")].copy()
vuelos_cordoba_df["fecha"] = pd.to_datetime(vuelos_ar_df['indice_tiempo'])

######################
# Data cleaning      #
######################
# %%
vuelos_cordoba_df = vuelos_cordoba_df.groupby("fecha").agg(pasajeros=('pasajeros', 'sum'))
#%%
# Está completa la tabla de datos? No
# Hubo días durante la pandemia que no se registró ningún pasajero
date_range = pd.date_range(start=vuelos_cordoba_df.index.min(),end= vuelos_cordoba_df.index.max(), freq="D")
vuelos_cordoba_df = vuelos_cordoba_df.sort_values("fecha")
vuelos_cordoba_df = vuelos_cordoba_df.reindex(date_range).reset_index()
vuelos_cordoba_df["pasajeros"] = vuelos_cordoba_df["pasajeros"].fillna(0)
vuelos_cordoba_df
# %%
####################
# Train, test and validation
end_train = pd.to_datetime("01-02-2023")
end_test = pd.to_datetime("01-02-2024")
train_vuelos_cordoba_df = vuelos_cordoba_df[(vuelos_cordoba_df['index'] <= end_train)].copy()
test_vuelos_cordoba_df = vuelos_cordoba_df[(vuelos_cordoba_df["index"] > end_train) & (vuelos_cordoba_df["index"] <= end_test)].copy() 
validate_vuelos_cordoba_df = vuelos_cordoba_df[vuelos_cordoba_df["index"] > end_test].copy()
print(f"Training will go from {train_vuelos_cordoba_df['index'].min()} to {train_vuelos_cordoba_df['index'].max()}")
print(f"Training will go from {test_vuelos_cordoba_df['index'].min()} to {test_vuelos_cordoba_df['index'].max()}")
print(f"Training will go from {validate_vuelos_cordoba_df['index'].min()} to {validate_vuelos_cordoba_df['index'].max()}")

#%%