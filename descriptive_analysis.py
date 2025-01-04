#%%
import matplotlib.pyplot as plt
import pandas as pd

vuelos_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/base_microdatos.csv")
vuelos_ar_df = vuelos_df[(vuelos_df["clasificacion_vuelo"] == "Cabotaje")].copy()
vuelos_ar_df["fecha"] = pd.to_datetime(vuelos_ar_df['indice_tiempo'])

# %%
# Cantidad pasajeros por año
vuelos_ar_df['year'] = vuelos_ar_df['fecha'].dt.year  # Extract the year

# Group by year and sum passengers
yearly_passengers = vuelos_ar_df.groupby('year')['pasajeros'].sum()

# Create the plot
fig, ax = plt.subplots(figsize=(8, 4))
yearly_passengers.plot(kind='bar', ax=ax)
# %%
# Borro los años 2020 y 2021
vuelos_ar_df = vuelos_ar_df[~vuelos_ar_df['year'].isin([2020, 2021])]
#%%
# Cantidad pasajeros por mes
vuelos_ar_df['month'] = vuelos_ar_df['fecha'].dt.month  # Extract the year
monthly_passengers = vuelos_ar_df.groupby('month')['pasajeros'].sum()

# Create the plot
fig, ax = plt.subplots(figsize=(8, 4))
monthly_passengers.plot(kind='bar', ax=ax)
# %%
# Cantidad pasajeros por mes y año
monthly_yearly_passengers = vuelos_ar_df.groupby(["year", "month"])['pasajeros'].sum().reset_index()

# Create the plot
fig, ax = plt.subplots(figsize=(8, 4))
monthly_yearly_passengers.plot(kind='bar', ax=ax)
# %%
# Aeropuertos con más vuelos cada año
top_airports_df = vuelos_ar_df.groupby("origen_aeropuerto")["pasajeros"].sum()
top_airports_df = top_airports_df.sort_values(ascending=False)[0:15]
fig, ax = plt.subplots(figsize=(8, 4))
top_airports_df.plot(kind='bar', ax=ax)
# %%
# Aeropuertos con más vuelos cada año
top_airports_df = vuelos_ar_df.groupby("destino_aeropuerto")["pasajeros"].sum()
top_airports_df = top_airports_df.sort_values(ascending=False)[0:15]
fig, ax = plt.subplots(figsize=(8, 4))
top_airports_df.plot(kind='bar', ax=ax)
# %%
