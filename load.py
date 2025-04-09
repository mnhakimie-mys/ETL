import pandas as pd
from transform import transform_data
import sqlite3

# Load file and execute transform
input_file = 'mudah_car_listings.csv'
df_clean = transform_data(input_file)

# Save database to CSV file
df_clean.to_csv("mudah_car_listings_clean.csv", index=False)
print("Saved to CSV: mudah_car_listings_clean.csv")

# Save to SQLite database file
conn = sqlite3.connect("mudah_car_listings.db")
df_clean.to_sql("car_listings", conn, if_exists="replace", index=False) # Table name: car_listings
conn.close()
print("Saved into SQLite DB: mudah_car_listings.db")

print("Database Saved completed.")
