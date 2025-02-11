# %%
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats

vuelos_df = pd.read_csv("/home/leontxo/Documents/maps_argentina/base_microdatos.csv")
vuelos_ar_df = vuelos_df[(vuelos_df["clasificacion_vuelo"] == "Cabotaje")].copy()
vuelos_ar_df["fecha"] = pd.to_datetime(vuelos_ar_df["indice_tiempo"])
# %%
plt.figure(figsize=(10, 6))

# Loop through each unique value in the "vuelos" column
for i, vuelo in enumerate(vuelos_ar_df["vuelos"].unique()):
    sum_of_all_flights = len(vuelos_ar_df[vuelos_ar_df["vuelos"] == vuelo])
    data = vuelos_ar_df[vuelos_ar_df["vuelos"] == vuelo]["asientos"]

    asientos_sum = data.sum()
    average_pasajeros = asientos_sum / sum_of_all_flights
    print(
        f"The average amountof seats offered for {vuelo} flight per day is: {round(average_pasajeros)}"
    )
    plt.bar(
        vuelo,
        average_pasajeros,
        alpha=0.6,
        label=f"Vuelos = {vuelo}",
        edgecolor="black",
    )

# Add labels and title
plt.xlabel("Vuelos")
plt.ylabel("Sum of Asientos")
plt.title("Sum of Asientos for Each Vuelos")

# Add a legend
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
# %%
vuelos_ar_df["year"] = vuelos_ar_df["fecha"].dt.year
pasajeros_sum_2023_cordoba = vuelos_ar_df[
    (
        (vuelos_ar_df["year"] == 2023)
        & (
            (vuelos_ar_df["destino_localidad"] == "Córdoba")
            | (vuelos_ar_df["origen_localidad"] == "Córdoba")
        )
    )
]["pasajeros"].sum()


# %%
# Cantidad pasajeros por año
vuelos_ar_df["year"] = vuelos_ar_df["fecha"].dt.year  # Extract the year

# Group by year and sum passengers
yearly_passengers = vuelos_ar_df.groupby("year")["pasajeros"].sum()

# Create the plot
fig, ax = plt.subplots(figsize=(8, 4))
yearly_passengers.plot(kind="bar", ax=ax)
# %%
# Borro los años 2020 y 2021
vuelos_ar_df = vuelos_ar_df[~vuelos_ar_df["year"].isin([2020, 2021])]
# %%
# Cantidad pasajeros por mes
vuelos_ar_df["month"] = vuelos_ar_df["fecha"].dt.month  # Extract the month
monthly_passengers = vuelos_ar_df.groupby("month")["pasajeros"].sum()

# Create the plot
fig, ax = plt.subplots(figsize=(8, 4))
monthly_passengers.plot(kind="bar", ax=ax)
# %%
# Cantidad pasajeros por mes y año
monthly_yearly_passengers = (
    vuelos_ar_df.groupby(["year", "month"])["pasajeros"].sum().reset_index()
)

# Create the plot
fig, ax = plt.subplots(figsize=(8, 4))
monthly_yearly_passengers.plot(kind="bar", ax=ax)
# %%
# Combinaciones de vuelos más comunes
vuelos_ar_df["combinaciones_provincias"] = vuelos_ar_df.apply(
    lambda row: tuple(sorted([row["origen_provincia"], row["destino_provincia"]])),
    axis=1,
)
top_provincias_df = vuelos_ar_df.groupby(["combinaciones"])["pasajeros"].sum()
top_provincias_df = top_provincias_df.sort_values(ascending=False)[0:25]
fig, ax = plt.subplots(figsize=(8, 4))
top_provincias_df.plot(kind="bar", ax=ax)


# %%
# Provincias con más pasajeros
top_provincias_df = vuelos_ar_df.groupby(["origen_provincia"])["pasajeros"].sum()
top_provincias_df = top_provincias_df.sort_values(ascending=False)[0:15]
fig, ax = plt.subplots(figsize=(8, 4))
top_provincias_df.plot(kind="bar", ax=ax)
# %%
# Aeropuerto con más vuelos cada año
top_provincias_df = vuelos_ar_df.groupby("destino_aeropuerto")["pasajeros"].sum()

top_provincias_df = top_provincias_df.sort_values(ascending=False)[0:15]
fig, ax = plt.subplots(figsize=(8, 4))
top_provincias_df.plot(kind="bar", ax=ax)
# %%
# Top aerolineas
top_provincias_df = vuelos_ar_df.groupby(["aerolinea", "year"])["pasajeros"].sum()

top_provincias_df = top_provincias_df.sort_values(ascending=False)[0:15]
fig, ax = plt.subplots(figsize=(8, 4))
top_provincias_df.plot(kind="bar", ax=ax)
# %%
