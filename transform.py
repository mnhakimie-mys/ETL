import pandas as pd

car_brands = [
    "Perodua", "Proton", "Toyota", "Honda", "Nissan", "Mazda", "Mitsubishi", "Hyundai", "Kia",
    "Ford", "Chevrolet", "Volkswagen", "Suzuki", "Peugeot", "Subaru", "Isuzu", "Volvo",
    "BMW", "Mercedes", "Audi", "Lexus", "Renault", "Chery", "Geely", "Great Wall", "Mini",
    "Jaguar", "Land Rover", "Porsche", "Alfa Romeo", "SsangYong", "Haval", "BYD", "Smart",
    "Tesla", "Infiniti", "Daihatsu", "Saab", "Changan", "FAW", "Tata"
]

def extract_brand(title):
    for brand in car_brands:
        if brand.lower() in title.lower():
            return brand
    return "Unknown"

def extract_model(title, brand):
    if brand != "Unknown":
        # Find the position of the brand in the title
        start_index = title.lower().find(brand.lower())
        # Extract the part of the title after the brand
        remaining_title = title[start_index + len(brand):].strip()
        # Split the remaining title and return the first word as the model
        return remaining_title.split(' ')[0]
    return "Unknown"

def transform_data(filepath):
    df = pd.read_csv(filepath)

    # Clean Price column
    df['Price'] = (
        df['Price']
        .str.replace('RM', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
        .replace('', '0')
        .astype(float)
        .round(2)
    )

    # Clean Mileage column
    def extract_avg_mileage(val):
        if pd.isna(val):
            return None
        try:
            nums = [int(x) for x in val.replace(',', '').split(' - ') if x.isdigit()]
            return int(sum(nums) / len(nums)) if nums else None
        except:
            return None

    df['Mileage'] = (
        df['Mileage']
        .apply(extract_avg_mileage)
    )    
    
    # Clean Year column
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    # Clean Engine Capacity column
    df['Engine Capacity'] = (
        df['Engine Capacity']
        .str.replace('cc', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
        .replace('', '0')
        .astype(int)
    )
    
    df.loc[df['Engine Capacity'] < 600, 'Engine Capacity'] = pd.NA
   
    # Extract Brand from Title
    df['Brand'] = df['Title'].apply(extract_brand)
    # Extract Model Name from Title
    # Access by row (use axis=1, because need information from two column title and brand (new column)
    df['Model'] = df.apply(lambda row: extract_model(row['Title'], row['Brand']), axis=1)
    
    return df

# Check the transformed file
if __name__ == "__main__":
    df = transform_data('mudah_car_listings.csv')
    #print(df.head())