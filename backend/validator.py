import pandas as pd
import numpy as np

coreFeatures = [
    'koi_model_snr',
    'koi_prad',
    'koi_depth',
    'koi_impact',
    'koi_period',
    'koi_duration'
]

optionalFeatures = [
    'koi_teq',
    'koi_steff',
    'koi_insol',
    'koi_srad',
    'koi_slogg'
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
    df['duration_ratio'] = df['koi_duration'] / (df['koi_period'] + 1e-6)

    # 5. Return in model’s expected column order
    features = coreFeatures +optionalFeatures + ['duration_ratio']
    return df[['planet_name'] + features]