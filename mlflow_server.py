#%%
from mlflow import MlflowClient
from pprint import pprint
from sklearn.ensemble import RandomForestRegressor

# %%
import subprocess
import time

# Start the MLflow server
mlflow_server_process = subprocess.Popen(
    [
        "mlflow", "server",
        "--backend-store-uri", "./mlruns",  # Local file store for metadata
        "--default-artifact-root", "./mlruns",  # Local directory for artifacts
        "--port", "5000"  # Port for the MLflow UI
    ]
)

# Wait for the server to start
time.sleep(5)

print("MLflow server is running at http://localhost:5000")

# %%
