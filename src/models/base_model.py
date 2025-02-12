#%%
import os
from dotenv import load_dotenv
from pathlib import Path

import pandas as pd

from skforecast.recursive import ForecasterEquivalentDate
from skforecast.model_selection import TimeSeriesFold
from skforecast.model_selection import backtesting_forecaster
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

mlflow.set_experiment("Base forecasting model")

train_flights_data_path = Path(os.getenv("BASE_DIR")) / "data" / "cleaned" / "cordoba" / "20170101_20230102_train.csv"
test_flights_data_path = Path(os.getenv("BASE_DIR")) / "data" / "cleaned" / "cordoba" / "20230103_20240102_test.csv"

test_cordoba_df = pd.read_csv(test_flights_data_path)
train_cordoba_df = pd.read_csv(train_flights_data_path)
train_cordoba_df["fecha"] = pd.to_datetime(train_cordoba_df["fecha"])
test_cordoba_df["fecha"] = pd.to_datetime(test_cordoba_df["fecha"])
train_cordoba_df = train_cordoba_df.set_index("fecha")
test_cordoba_df = test_cordoba_df.set_index("fecha")
train_cordoba_df = train_cordoba_df.asfreq("D") 
test_cordoba_df = test_cordoba_df.asfreq("D") 
#%%
with mlflow.start_run():

    forecaster = ForecasterEquivalentDate(
                    offset  = pd.DateOffset(days=1),
                    n_offsets = 12
             )
# %%
    forecaster.fit(y=test_cordoba_df.loc[:, 'pasajeros'])
    forecaster
# %%
    cv = TimeSeriesFold(steps = 2,
            initial_train_size = len(test_cordoba_df),
            refit              = False
    )
    metrica, predicciones = backtesting_forecaster(
                            forecaster    = forecaster,
                            y             = train_cordoba_df['pasajeros'],
                            cv            = cv,
                            metric        = 'mean_absolute_error',
                            n_jobs        = 'auto',
                            verbose       = False,
                            show_progress = True
                        )
# %%
    mlflow.log_param("initial_train_size", len(test_cordoba_df))
    mlflow.log_metric("metrica", metrica["mean_absolute_error"])
    mlflow.log_artifact(Path(os.getenv("BASE_DIR"))/ "mlruns" / "base_model.txt")  # Log a file as an artifact
    print("Run logged successfully!")
# %%
