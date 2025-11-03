import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from transform_weather import transform_weather_data

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

def get_db_engine():
    conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn_str)

def load_to_postgres(df, table_name="weather_data"):
    engine = get_db_engine()
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Successfully inserted {len(df)} records into '{table_name}' table.")

def main():
    df = transform_weather_data("weather_data.csv")
    load_to_postgres(df)

if __name__ == "__main__":
    main()