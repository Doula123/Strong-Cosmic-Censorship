import pandas as pd



data = pd.read_csv("Kepler.csv",comment = '#')
data2 = pd.read_csv("K2.csv",comment = '#')
data3 = pd.read_csv("TESS.csv",comment = '#')




k2 = data2.rename(columns={
    'pl_orbper': 'koi_period',
    'pl_rade': 'koi_prad',
    'st_rad': 'koi_srad',
    'st_teff': 'koi_steff',
    'st_logg': 'koi_slogg',
    'pl_eqt': 'koi_teq',
    'pl_insol': 'koi_insol',
    'disposition': 'koi_disposition'
})

for col in ['koi_duration', 'koi_depth', 'koi_impact', 'koi_model_snr']:
    if col not in k2.columns:
        k2[col] = float('nan')

label_map = {'FP':'FALSE POSITIVE', 'PC':'CANDIDATE', 'CP':'CONFIRMED'}
data3['koi_disposition'] = data3['tfopwg_disp'].map(label_map)

tess = data3.rename(columns={
    'pl_orbper':   'koi_period',
    'pl_trandurh': 'koi_duration',
    'pl_trandep':  'koi_depth',
    'pl_rade':     'koi_prad',
    'st_rad':      'koi_srad',
    'st_teff':     'koi_steff',
    'st_logg':     'koi_slogg',
    'pl_eqt':      'koi_teq',
    'pl_insol':    'koi_insol'
})

for col in ['koi_model_snr','koi_impact']:
    if col not in tess.columns:
        tess[col] = float('nan')

tess = tess.dropna(subset=['koi_disposition'])


features = [
    'koi_period',
    'koi_duration',
    'koi_depth',
    'koi_prad',
    'koi_srad',
    'koi_model_snr',
    'koi_impact', 
    'koi_steff',
    'koi_slogg',
    'koi_teq',     
    'koi_insol'
    
]
print(set(features) - set(k2.columns))

print(data.columns.tolist())
target = 'koi_disposition'
data_clean = data[features + [target]].copy()
k2_clean = k2[features + [target]].copy()
tess_clean   = tess[features + [target]].copy()

print("Kepler:", data_clean.shape)
print("K2,", k2_clean.shape)
print("TESS:", tess_clean.shape)

combined = pd.concat([data_clean,k2_clean, tess_clean],ignore_index=True)
print("Combined,", combined.shape)





combined.to_csv("CleanedKepler.csv", index=False)
