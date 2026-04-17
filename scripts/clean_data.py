from pathlib import Path
import pandas as pd


# File paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "eea_s_eu-sdg-nuts23-11-52_p_2005-2023_v01_r00.csv"
CLEANED_FILE = BASE_DIR / "data" / "cleaned" / "eea_air_pollution_cleaned.csv"


def load_data(file_path: Path) -> pd.DataFrame:
    """Load raw CSV dataset."""
    return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the EEA dataset for Streamlit dashboard use."""
    
    # Standardise column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Drop fully empty columns
    df = df.dropna(axis=1, how="all")

    # Drop constant columns that add no dashboard value
    constant_cols = [col for col in df.columns if df[col].nunique(dropna=False) == 1]
    if "code" in constant_cols:
        df = df.drop(columns=["code"])

    # Remove duplicate rows if any
    df = df.drop_duplicates()

    # Clean text fields
    text_cols = ["dimension", "dimension_label", "unit", "unit_label", "geo", "geo_label"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Rename columns to more readable names
    df = df.rename(columns={
        "dimension": "indicator_code",
        "dimension_label": "indicator_name",
        "geo": "region_code",
        "geo_label": "region_name",
        "time": "year",
        "obs_value": "value"
    })

    # Ensure proper data types
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Optional: create shorter labels for dashboard filters
    indicator_map = {
        "PMD": "Premature deaths",
        "YLL": "Years of life lost"
    }
    if "indicator_code" in df.columns:
        df["indicator_short"] = df["indicator_code"].map(indicator_map).fillna(df["indicator_code"])

    # Reorder columns nicely
    preferred_order = [
        "indicator_code",
        "indicator_short",
        "indicator_name",
        "unit",
        "unit_label",
        "region_code",
        "region_name",
        "year",
        "value"
    ]
    existing_cols = [col for col in preferred_order if col in df.columns]
    remaining_cols = [col for col in df.columns if col not in existing_cols]
    df = df[existing_cols + remaining_cols]

    return df


def save_data(df: pd.DataFrame, output_path: Path) -> None:
    """Save cleaned data."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main():
    df = load_data(RAW_FILE)

    print("Raw shape:", df.shape)
    print("\nMissing values:")
    print(df.isna().sum())

    cleaned_df = clean_data(df)

    print("\nCleaned shape:", cleaned_df.shape)
    print("\nColumns:")
    print(cleaned_df.columns.tolist())

    print("\nPreview:")
    print(cleaned_df.head())

    save_data(cleaned_df, CLEANED_FILE)
    print(f"\nCleaned file saved to: {CLEANED_FILE}")


if __name__ == "__main__":
    main()