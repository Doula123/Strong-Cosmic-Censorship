# backend/Cleandata.py
import pandas as pd
import numpy as np

def clean_uploaded_dataset(file_obj):
    """
    Cleans a single uploaded CSV file (Kepler, K2 or TESS)
    and returns a standardized DataFrame.
    file_obj can be a Flask uploaded file or a file path.
    """

    # Read CSV while ignoring comment lines
    df_raw = pd.read_csv(file_obj, comment='#')

    cols = set(df_raw.columns)

    # --------- KEPLER ----------
    if 'koi_period' in cols:
        df = df_raw.rename(columns={
            'koi_period': 'orb_period',
            'koi_duration': 'duration',
            'koi_depth': 'depth',
            'koi_prad': 'planet_rad',
            'koi_srad': 'stellar_rad',
            'koi_model_snr': 'model_snr',
            'koi_impact': 'impact',
            'koi_steff': 'stellar_teff',
            'koi_slogg': 'stellar_g_log',
            'koi_teq': 'planet_eq_temp',
            'koi_insol': 'planet_insol',
            'koi_disposition': 'disposition'
        })
        if 'kepid' in df_raw.columns:
            df['planet_name'] = df_raw['kepid']

    # --------- K2 ----------
    elif 'pl_orbper' in cols and 'pl_rade' in cols:
        df = df_raw.rename(columns={
            'pl_orbper': 'orb_period',
            'pl_rade': 'planet_rad',
            'st_rad': 'stellar_rad',
            'st_teff': 'stellar_teff',
            'st_logg': 'stellar_g_log',
            'pl_eqt': 'planet_eq_temp',
            'pl_insol': 'planet_insol',
            'disposition': 'disposition'
        })

        # add missing columns so that all missions have the same set
        for col in ['duration', 'depth', 'impact', 'model_snr']:
            if col not in df.columns:
                df[col] = np.nan

        if 'pl_name' in df_raw.columns:
            df['planet_name'] = df_raw['pl_name']

    # --------- TESS ----------
    elif 'tfopwg_disp' in cols:
        label_map = {'FP': 'FALSE POSITIVE', 'PC': 'CANDIDATE', 'CP': 'CONFIRMED'}
        df_raw['disposition'] = df_raw['tfopwg_disp'].map(label_map)

        df = df_raw.rename(columns={
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

        for col in ['model_snr', 'impact']:
            if col not in df.columns:
                df[col] = np.nan

        if 'toi' in df_raw.columns:
            df['planet_name'] = df_raw['toi']

        # drop rows that have no final disposition
        df = df.dropna(subset=['disposition'])

    else:
        raise ValueError("Unrecognized CSV format: not Kepler, K2 or TESS")

    # ---- Verify planet_name ----
    if 'planet_name' not in df.columns:
        raise ValueError("No 'planet_name' column could be derived from this file")

    # ---- Ensure full feature set ----
    features = [
        'orb_period', 'duration', 'depth',
        'planet_rad', 'stellar_rad',
        'model_snr', 'impact',
        'stellar_teff', 'stellar_g_log',
        'planet_eq_temp', 'planet_insol'
    ]

    for f in features:
        if f not in df.columns:
            df[f] = np.nan

    # Keep only the standardized columns (plus disposition if available)
    final_cols = ['planet_name'] + features
    if 'disposition' in df.columns:
        final_cols.append('disposition')

    return df[final_cols]
