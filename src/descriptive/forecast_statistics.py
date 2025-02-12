# %%
import os
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

# %%
load_dotenv()
flights_data_path = Path(os.getenv("BASE_DIR")) / "data" / "raw" / "base_microdatos.csv"

vuelos_df = pd.read_csv(flights_data_path)
vuelos_ar_df = vuelos_df[(vuelos_df["clasificacion_vuelo"] == "Cabotaje")].copy()
vuelos_cordoba_df = vuelos_ar_df[
    (vuelos_ar_df["origen_provincia"] == "Córdoba")
    | (vuelos_ar_df["destino_provincia"] == "Córdoba")
].copy()
vuelos_cordoba_df["fecha"] = pd.to_datetime(vuelos_ar_df["indice_tiempo"])

######################
# Data cleaning      #
######################
# %%
vuelos_cordoba_df = vuelos_cordoba_df.groupby("fecha").agg(
    pasajeros=("pasajeros", "sum")
)
# %%
# Está completa la tabla de datos? No
# Hubo días durante la pandemia que no se registró ningún pasajero
date_range = pd.date_range(
    start=vuelos_cordoba_df.index.min(), end=vuelos_cordoba_df.index.max(), freq="D"
)

vuelos_cordoba_df = vuelos_cordoba_df.sort_values("fecha")
vuelos_cordoba_df = vuelos_cordoba_df.reindex(date_range)
vuelos_cordoba_df["pasajeros"] = vuelos_cordoba_df["pasajeros"].fillna(0).astype("int")
vuelos_cordoba_df = vuelos_cordoba_df.reset_index()
vuelos_cordoba_df = vuelos_cordoba_df.rename(columns={"index": "fecha"})
# %%
###COVID
covid_start = pd.to_datetime("01-02-2020")
covid_end = pd.to_datetime("01-04-2022")
vuelos_cordoba_df["covid"] = np.where(
    (vuelos_cordoba_df["fecha"] >= covid_start)
    & (vuelos_cordoba_df["fecha"] < covid_end),
    1,
    0,
)
# %%
# Save the file to train.
min_date = vuelos_cordoba_df["fecha"].min().strftime("%Y%m%d")
max_date = vuelos_cordoba_df["fecha"].max().strftime("%Y%m%d")
flights_ready_data_path = Path(os.getenv("BASE_DIR")) / "data" / "cleaned" / "cordoba"/ f"0_{min_date}_{max_date}_full_data.csv"

vuelos_cordoba_df.to_csv(flights_ready_data_path, index=False)


#%%
####################
# Train, test and validation
end_train = pd.to_datetime("01-02-2022")
end_test = pd.to_datetime("01-02-2024")

train_vuelos_cordoba_df = vuelos_cordoba_df[
    (vuelos_cordoba_df["fecha"]  <= end_train)
]
test_vuelos_cordoba_df = vuelos_cordoba_df[
    (vuelos_cordoba_df["fecha"]  > end_train) & (vuelos_cordoba_df["fecha"]  <= end_test)
]
validate_vuelos_cordoba_df = vuelos_cordoba_df[
    vuelos_cordoba_df["fecha"]  > end_test
]
print(
    f"Training will go from {train_vuelos_cordoba_df['fecha'].min()} to {train_vuelos_cordoba_df['fecha'].max()}"
)
print(
    f"Testing will go from {test_vuelos_cordoba_df['fecha'].min()} to {test_vuelos_cordoba_df['fecha'].max()}"
)
print(
    f"Validation will go from {validate_vuelos_cordoba_df['fecha'].min()} to {validate_vuelos_cordoba_df['fecha'].max()}"
)
#%%
#Save test, train and validation in different files
min_date = train_vuelos_cordoba_df["fecha"].min().strftime("%Y%m%d")
max_date = train_vuelos_cordoba_df["fecha"].max().strftime("%Y%m%d")
train_vuelos_cordoba_df_path = Path(os.getenv("BASE_DIR")) / "data" / "cleaned" / "cordoba" / f"{min_date}_{max_date}_train.csv"

train_vuelos_cordoba_df.to_csv(train_vuelos_cordoba_df_path, index=False)

min_date = test_vuelos_cordoba_df["fecha"].min().strftime("%Y%m%d")
max_date = test_vuelos_cordoba_df["fecha"].max().strftime("%Y%m%d")
test_vuelos_cordoba_df_path = Path(os.getenv("BASE_DIR")) / "data" / "cleaned" / "cordoba" / f"{min_date}_{max_date}_test.csv"

test_vuelos_cordoba_df.to_csv(test_vuelos_cordoba_df_path, index=False)

min_date = validate_vuelos_cordoba_df["fecha"].min().strftime("%Y%m%d")
max_date = validate_vuelos_cordoba_df["fecha"].max().strftime("%Y%m%d")
validate_vuelos_cordoba_df_path = Path(os.getenv("BASE_DIR")) / "data" / "cleaned" / "cordoba" / f"{min_date}_{max_date}_validation.csv"

validate_vuelos_cordoba_df.to_csv(validate_vuelos_cordoba_df_path, index=False)


# %%
# Data visualization

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=train_vuelos_cordoba_df["fecha"],
        y=train_vuelos_cordoba_df["pasajeros"],
        mode="lines",
        name="Train",
    )
)
fig.add_trace(
    go.Scatter(
        x=test_vuelos_cordoba_df["fecha"],
        y=test_vuelos_cordoba_df["pasajeros"],
        mode="lines",
        name="test",
    )
)
fig.add_trace(
    go.Scatter(
        x=validate_vuelos_cordoba_df["fecha"],
        y=validate_vuelos_cordoba_df["pasajeros"],
        mode="lines",
        name="validation",
    )
)
fig.update_layout(
    title="Pasajeros domésticos de Córdoba",
    xaxis_tickformat="%Y-%m-%d",
    yaxis_title="Pasajeros",
    legend_title="Partición:",
    width=750,
    height=370,
    margin=dict(l=20, r=20, t=35, b=20),
    legend=dict(orientation="h", yanchor="top", y=1, xanchor="left", x=0.001),
)
# %%
# Seasonality weekly, monthly and annually
fig, axs = plt.subplots(2, 2, figsize=(8, 5), sharex=False, sharey=True)
axs = axs.ravel()

vuelos_cordoba_df["mes"] = vuelos_cordoba_df["fecha"].month
vuelos_cordoba_df[vuelos_cordoba_df["covid"] == 0].boxplot(
    column="pasajeros", by="mes", ax=axs[0], flierprops={"markersize": 3, "alpha": 0.3}
)
vuelos_cordoba_df[vuelos_cordoba_df["covid"] == 0].groupby("mes")[
    "pasajeros"
].median().plot(style="o-", linewidth=0.8, ax=axs[0])
axs[0].set_ylabel("pasajeros")
axs[0].set_title("Distribución de pasajeros por mes. Ex Covid", fontsize=9)

vuelos_cordoba_df.boxplot(
    column="pasajeros", by="mes", ax=axs[1], flierprops={"markersize": 3, "alpha": 0.3}
)
vuelos_cordoba_df.groupby("mes")["pasajeros"].median().plot(
    style="o-", linewidth=0.8, ax=axs[1]
)
axs[1].set_ylabel("pasajeros")
axs[1].set_title("Pasajeros por mes", fontsize=9)

vuelos_cordoba_df["semana"] = vuelos_cordoba_df["fecha"].day_of_week + 1
vuelos_cordoba_df[vuelos_cordoba_df["covid"] == 0].boxplot(
    column="pasajeros",
    by="semana",
    ax=axs[2],
    flierprops={"markersize": 3, "alpha": 0.3},
)
vuelos_cordoba_df[vuelos_cordoba_df["covid"] == 0].groupby("semana")[
    "pasajeros"
].median().plot(style="o-", linewidth=0.8, ax=axs[2])
axs[2].set_ylabel("pasajeros")
axs[2].set_title("Pasajeros por semana. Ex Covid", fontsize=9)

vuelos_cordoba_df.boxplot(
    column="pasajeros",
    by="semana",
    ax=axs[3],
    flierprops={"markersize": 3, "alpha": 0.3},
)
vuelos_cordoba_df.groupby("semana")["pasajeros"].median().plot(
    style="o-", linewidth=0.8, ax=axs[3]
)
axs[3].set_ylabel("pasajeros")
axs[3].set_title("Pasajeros por semana", fontsize=9)


fig.suptitle("Gráficos de estacionalidad sin y con Covid", fontsize=12)
fig.tight_layout()
# %%
fig, ax = plt.subplots(figsize=(20, 2))
plot_pacf(
    vuelos_cordoba_df[vuelos_cordoba_df["covid"] == 0]["pasajeros"], ax=ax, lags=50
)
plt.show()
# %%
fig, ax = plt.subplots(figsize=(20, 2))
plot_acf(
    vuelos_cordoba_df[vuelos_cordoba_df["covid"] == 0]["pasajeros"], ax=ax, lags=50
)
plt.show()
# %%
