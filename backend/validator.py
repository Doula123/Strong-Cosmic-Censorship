import pandas as pd
import numpy as np
from .Cleandata import clean_uploaded_dataset

#core features
coreFeatures = [
    'orb_period',
    'duration',
    'depth',
    'planet_rad',
    'stellar_rad',
    'model_snr',
    'impact'
]

optionalFeatures = [
    'stellar_teff',
    'stellar_g_log',
    'planet_eq_temp',
    'planet_insol'
]
MODEL_FEATURE_ORDER = [
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
    'planet_insol',
    'duration_ratio'
]

def prepare_user_input(csv_path, min_core_required=3):


    df = clean_uploaded_dataset(csv_path)

    if 'planet_name' not in df.columns:
        raise ValueError("Your CSV must include a 'planet_name' column.")
    
    provided_core = [c for c in coreFeatures if c in df.columns and df[c].notna().any()]
    if len(provided_core) < min_core_required:
        raise ValueError(
            f"Please provide at least {min_core_required} of the core parameters: "
            f"{', '.join(coreFeatures)}.\n"
            f"Currently found: {', '.join(provided_core) if provided_core else 'none'}."
        )
    

    for c in MODEL_FEATURE_ORDER:
        if c not in df.columns:
            df[c] = np.nan

    # 4. Compute derived feature
    df['duration_ratio'] = df['duration'] / (df['orb_period'] + 1e-6)

    # 5. Return in model’s expected column order
    features = coreFeatures +optionalFeatures + ['duration_ratio']
    return df[['planet_name'] + MODEL_FEATURE_ORDER]