import pandas as pd

def transform_weather_data(csv_file="weather_data.csv"):
    
    print("Starting data cleaning process...")

    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} records from {csv_file}")

    # Remove duplicated city data with same timestamp
    df = df.drop_duplicates(subset=["city", "timestamp"])
    print(f"🗑️ Removed duplicates. Remaining: {len(df)} rows")

    # Remove rows with missing key values
    df = df.dropna(subset=["temperature", "humidity"])
    print(f"🔍 Removed missing values. Remaining: {len(df)} rows")

    # Round temperature and wind speed for consistency
    if "temperature" in df.columns:
        df["temperature"] = df["temperature"].round(1)
    if "wind_speed" in df.columns:
        df["wind_speed"] = df["wind_speed"].round(1)
    if "temp_min" in df.columns:
        df["temp_min"] = df["temp_min"].round(1)
    if "temp_max" in df.columns:
        df["temp_max"] = df["temp_max"].round(1)

    # Convert timestamp column to datetime type ---
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Remove rows with invalid timestamps (if any)
    df = df.dropna(subset=["timestamp"])

    # Reset index after cleaning ---
    df = df.reset_index(drop=True)

    print(f"Cleaned {len(df)} records ready for database load.\n")
    return df

if __name__ == "__main__":
    transform_weather_data()
