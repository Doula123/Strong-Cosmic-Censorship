import pandas as pd



data = pd.read_csv("Kepler.csv",comment = '#')


features = 
[
    'koi_period'
    'koi_duration'
    'koi_depth'
    'koi_prad'
    'koi_srad'
    'koi_model_snr'
]

target = 'koi_disposition'
data = data[features + [target]].copy()
print()
