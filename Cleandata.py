import pandas as pd

data = pd.read_csv("Kepler.csv",comment = '#')
data2 = pd.read_csv("K2.csv",comment = '#')
data3 = pd.read_csv("TESS.csv",comment = '#')

kepler = data.rename(columns={ 'koi_period' : 'orb_period',
                               'koi_duration' : 'duration',
                               'koi_depth' : 'depth',
                               'koi_prad' :'planet_rad',
                               'koi_srad': 'stellar_rad',
                               'koi_model_snr' : 'model_snr', #signal-noise ratio
                               'koi_impact' : 'impact',
                                'koi_steff' : 'stellar_teff',
                               'koi_slogg' : 'stellar_g_log',
                               'koi_teq' : 'planet_eq_temp' ,
                               'koi_insol' : 'planet_insol',
                               'koi_disposition' : 'disposition'})

k2 = data2.rename(columns={
    'pl_orbper' : 'orb_period', #orbital period (days)
    'pl_rade': 'planet_rad', #planetary radius (in Earth radii)
    'st_rad': 'stellar_rad', #stellar radius (Sun radii)
    'st_teff': 'stellar_teff', #stellar effective temperature (K)
    'st_logg': 'stellar_g_log', #stellar gravity (log) [[cm/s**2]]
    'pl_eqt': 'planet_eq_temp', #planet equilibrium temperature (K)
    'pl_insol': 'planet_insol', #planet insolation (Earth Flux)
    'disposition': 'disposition'
})

for col in ['duration', 'depth', 'impact', 'model_snr']:
    if col not in k2.columns:
        k2[col] = float('nan')

label_map = {'FP':'FALSE POSITIVE', 'PC':'CANDIDATE', 'CP':'CONFIRMED'}
data3['disposition'] = data3['tfopwg_disp'].map(label_map)

tess = data3.rename(columns={
    'pl_orbper': 'orb_period',
    'pl_trandurh': 'duration',
    'pl_trandep': 'depth',
    'pl_rade': 'planet_rad',
    'st_rad': 'stellar_rad',
    'st_teff': 'stellar_teff',
    'st_logg': 'stellar_g_log',
    'pl_eqt': 'planet_eq_temp',
    'pl_insol': 'planet_insol'
})


for col in ['model_snr','impact']:
    if col not in tess.columns:
        tess[col] = float('nan')

if 'pl_name' in k2.columns:
    k2['planet_name'] = k2['pl_name']

if 'toi' in tess.columns:
    tess['planet_name'] = tess['toi']
if 'kepid' in data.columns:
    kepler['planet_name'] = kepler['kepid']


tess = tess.dropna(subset=['disposition'])


features = [
    'orb_period',
    'duration',
    'depth',
    'planet_rad',
    'stellar_rad',
    'model_snr',
    'impact',
    'stellar_teff',
    'stellar_g_log',
    'planet_eq_temp',
    'planet_insol'
]

print(set(features) - set(k2.columns))

print(data.columns.tolist())
target = 'disposition'
data_clean = kepler[['planet_name'] + features + [target]].copy()
k2_clean = k2[['planet_name'] + features + [target]].copy()
tess_clean   = tess[['planet_name'] + features + [target]].copy()

print("Kepler:", data_clean.shape)
print("K2,", k2_clean.shape)
print("TESS:", tess_clean.shape)

combined = pd.concat([data_clean,k2_clean, tess_clean],ignore_index=True)
print("Combined,", combined.shape)





combined.to_csv("CleanedKepler.csv", index=False)
