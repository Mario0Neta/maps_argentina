#%%
import os
from dotenv import load_dotenv
from pathlib import Path

import pandas as pd

from skforecast.recursive import ForecasterEquivalentDate

load_dotenv()
flights_data_path = Path(os.getenv("BASE_DIR")) / "data" / "cleaned" / "cordoba" / "20170101_20230102_train.csv"

train_cordoba_df = pd.read_csv(flights_data_path)
train_cordoba_df = train_cordoba_df.set_index("fecha")
train_cordoba_df = train_cordoba_df.asfreq("D") 
#%%

forecaster = ForecasterEquivalentDate(
                 offset  = pd.DateOffset(days=1),
                 n_offsets = 1
             )
# %%
forecaster.fit(y=train_cordoba_df.loc[:, 'pasajeros'])
forecaster
# %%
