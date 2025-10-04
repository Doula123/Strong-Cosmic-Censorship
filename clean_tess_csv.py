import pandas as pd
import csv

INPUT_FILE = "TESS.csv"
OUTPUT_FILE = "TESS_cleaned.csv"

def detect_and_clean_csv(input_path, output_path):
    print(f"Checking {input_path} for malformed rows...")

    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_cols = len(header)
    print(f"Header has {expected_cols} columns")

    # skip bad line
    try:
        df = pd.read_csv(input_path, on_bad_lines="skip", low_memory=False)
        print(f" Loaded {len(df)} valid rows successfully.")
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    # drop completely empty rows
    df.dropna(how="all", inplace=True)

    # save cleaned version
    df.to_csv(output_path, index=False)
    print(f"Cleaned file saved as: {output_path}")
    print(f"Cleaned dataset shape: {df.shape}")

if __name__ == "__main__":
    detect_and_clean_csv(INPUT_FILE, OUTPUT_FILE)
