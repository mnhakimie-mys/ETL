from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd

# Launch Firefox browser
driver = webdriver.Firefox()

car_data = []

try:
    for page in range(1, 13):  # Scrape 12 pages
        url = f"https://www.mudah.my/malaysia/cars-for-sale?o={page}"
        driver.get(url)

        try:
            # Wait until listings load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid^="listing-ad-item"]'))
            )
        except TimeoutException:
            print(f"Timeout on page {page}")
            continue

        # Loop through all listings
        listings = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid^="listing-ad-item"]')
        print(f"Scraping page {page} with {len(listings)} listings...")
        
        for listing in listings:
            try:
                title = listing.find_element(By.CSS_SELECTOR, 'a[title]').get_attribute("title").strip()
            except NoSuchElementException:
                title = 'N/A'

            try:
                price = listing.find_element(By.XPATH, './/div[contains(text(), "RM")]').text.strip()
            except NoSuchElementException:
                price = 'N/A'

            def get_detail(label):
                try:
                    return listing.find_element(By.XPATH, f'.//div[@title="{label}"]/div').text.strip()
                except NoSuchElementException:
                    return 'N/A'

            condition = get_detail("Condition")
            mileage = get_detail("Mileage")
            engine = get_detail("Engine capacity")

            try:
                year_elem = listing.find_element(By.XPATH, './/div[@data-testid="year-verified-badge"]/div')
                year = year_elem.text.strip()
            except NoSuchElementException:
                year = 'N/A'

            car_data.append([title, price, condition, mileage, year, engine])

finally:
    driver.quit()

# Convert to DataFrame
df = pd.DataFrame(car_data, columns=['Title', 'Price', 'Condition', 'Mileage', 'Year', 'Engine Capacity'])
print(df)

# Save the scraped data to CSV
df.to_csv("mudah_car_listings.csv", index=False)
print("Saved to mudah_car_listings.csv")