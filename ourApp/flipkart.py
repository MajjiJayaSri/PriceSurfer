from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
from django.conf import settings
def scrap_Flipkart(search_ele):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = service)
    driver.get("https://www.flipkart.com/")
  # wait for at max 10 secs
    driver.implicitly_wait(10)
    driver.maximize_window()
    try:
        driver.find_element(By.XPATH, "//input[contains(@title,'Search')]").send_keys(search_ele)
        driver.find_element(By.XPATH, "//button[contains(@class,'2iLD_')]").click()
        
        prod_names = driver.find_elements(By.XPATH, "//div[contains(@class,'KzDlHZ')]") ## list
        prod_prices = driver.find_elements(By.XPATH, "//div[contains(@class,'_4b5DiR')]")
        prod_images = driver.find_elements(By.XPATH, "//img[contains(@loading,'eager')]")
        prod_links = driver.find_elements(By.XPATH, "//a[contains(@class,'CGtC98')]")
        #driver.quit()
        names_list = []
        price_list = []
        image_list = []
        links_list = []
        for names in prod_names:
            names_list.append(names.text)
        for prc in prod_prices:
            price_list.append(prc.text)
        for img in prod_images:
            image_list.append(img.get_attribute('src'))
        for link in prod_links:
            links_list.append(link.get_attribute('href'))
        print("all products listed")
        prod_data = {
            "Product Name" : names_list,
            "Price" : price_list,
            "Image Link": image_list,
            "Product Link" :links_list
        }
        print(settings.EXPORTS_ROOT)
        print(os.path.exists(settings.EXPORTS_ROOT))

        df = pd.DataFrame(prod_data)
        csv_file_path = os.path.join(settings.EXPORTS_ROOT, "flipkart_data.csv")
        df.to_csv(csv_file_path,index = False,mode='a')
        print("Data exported")
    except Exception as e:
        print("Error occured while storing to flipkart")
    finally:
        driver.quit()
        prod_details=zip(names_list,price_list,image_list,links_list)
        prod_details = list(prod_details)
        return prod_details