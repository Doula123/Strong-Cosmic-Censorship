import pandas as pd
import numpy as np

coreFeatures = [
    'model_snr',
    'planet_rad',
    'depth',
    'impact',
    'orb_period',
    'duration'
]

optionalFeatures = [
    'planet_eq_temp',
    'stellar_teff',
    'planet_insol',
    'stellar_rad',
    'stellar_g_log'
]

def prepare_user_input(csv_path, min_core_required=3):


    df = pd.read_csv(csv_path)

    if 'planet_name' not in df.columns:
        raise ValueError("Your CSV must include a 'planet_name' column.")
    
    provided_core = [c for c in coreFeatures if c in df.columns and df[c].notna().any()]
    if len(provided_core) < min_core_required:
        raise ValueError(
            f"Please provide at least {min_core_required} of the core parameters: "
            f"{', '.join(coreFeatures)}.\n"
            f"Currently found: {', '.join(provided_core) if provided_core else 'none'}."
        )
    

    for c in coreFeatures + optionalFeatures:
        if c not in df.columns:
            df[c] = np.nan

    # 4. Compute derived feature
    df['duration_ratio'] = df['duration'] / (df['orb_period'] + 1e-6)

    # 5. Return in model’s expected column order
    features = coreFeatures +optionalFeatures + ['duration_ratio']
    return df[['planet_name'] + features]