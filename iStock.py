import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize Chrome options and WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
driver = webdriver.Chrome(options=chrome_options)

# Base URL for iStockPhoto search
base_url = 'https://www.istockphoto.com/search/2/image?alloweduse=availableforalluses&mediatype=photography&phrase=nasi%20kandar&sort=best&page='

# Create a directory for saving images
os.makedirs("NasiKandarImages", exist_ok=True)
image_dir = "NasiKandarImages"

# Counter to keep track of downloaded images
image_counter = 0

# Function to scroll and download images
def scroll_and_download_images(scrolls):
    global image_counter
    for scroll in range(scrolls):
        url = base_url + str(scroll + 1)  # Change the page number in the URL
        driver.get(url)
        
        # Scroll to the bottom of the page to load all images
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Collect image elements
        image_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/section/div/main/div/div/div[2]/div[2]/div[3]//img')

        for i, img in enumerate(image_elements):
            image_url = img.get_attribute("src")
            if image_url:
                try:
                    image_data = requests.get(image_url, stream=True).content
                    with open(f"{image_dir}/nasi_kandar_{image_counter}.jpg", "wb") as image_file:
                        image_file.write(image_data)
                    print(f"Image {image_counter} downloaded")
                    image_counter += 1

                except Exception as e:
                    print(f"Error downloading image {i}: {e}")

# Specify the number of scrolls (pages)
scrolls = 50  # Download images from pages 1 to 5

scroll_and_download_images(scrolls)

# Close the browser
driver.quit()
