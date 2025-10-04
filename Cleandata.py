import pandas as pd



data = pd.read_csv("Kepler.csv",comment = '#')


features = [
    'koi_period',
    'koi_duration',
    'koi_depth',
    'koi_prad',
    'koi_srad',
    'koi_model_snr'
]

target = 'koi_disposition'
data = data[features + [target]].copy()
print(data.shape)



missing_counts = data[features].isnull().sum(axis=1)

##data = data[missing_counts < 1].copy()
print(data.shape)
#for col in features:
 #   if data[col].isnull().sum() > 0 :
    #    medianValue = data[col].median()
     #   data[col].fillna(medianValue, inplace=True)

data.to_csv("CleanedKepler.csv", index=False)
print(missing_counts.value_counts())