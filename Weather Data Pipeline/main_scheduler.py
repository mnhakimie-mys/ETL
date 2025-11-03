import time
import schedule
from extract_weather import main as extract_main
from transform_weather import transform_weather_data
from load_to_postgres import load_to_postgres
from load_to_postgres import get_db_engine

def job():
    print("⏰ Running scheduled weather ETL job...")
    
    # 1️ Extract
    extract_main()

    # 2 Transform
    df = transform_weather_data("weather_data.csv")

    # 3 Load
    load_to_postgres(df)
    print("✅ ETL cycle complete!\n")

# Schedule the job every 15 minutes
schedule.every(15).minutes.do(job)
print("🟢 Weather ETL Scheduler started — running every 15 minutes.")
job()

while True:
    schedule.run_pending()
    time.sleep(10)
