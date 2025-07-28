
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
from django.conf import settings
def ScrapAmazon(search):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.amazon.in/")
    driver.implicitly_wait(10)
    
    driver.find_element(By.XPATH,"//input[contains(@id, 'searchtext')]").send_keys(search)
    driver.find_element(By.XPATH,"//input[@value='Go']").click()
    time.sleep(3)
    names=driver.find_elements(By.XPATH,"//a[contains(@class,'s-line-clamp-2 s-link-style a-text-normal')]/h2/span")
    prices=driver.find_elements(By.XPATH,"//div[contains(@class,'a-spacing-top-micro puis')] /div/div/a/span//span[contains(@class,'a-offscreen')]")    
    images = driver.find_elements(By.XPATH, "//div[contains(@class,'a-section aok-relative s-image-fixed-height')]/img")
    links=driver.find_elements(By.XPATH,"//a[contains(@class, 'clamp-2')]")
    #driver.quit()
    names_list=[]
    prices_list=[]
    images_list=[]
    links_list=[]
    for i in names:
        names_list.append(i.text)
        
    for i in prices:
    #     print(i.text)
        prices_list.append(i.get_attribute("innerHTML")[:])

    for i in images:
        images_list.append(i.get_attribute("src"))
        
    for i in links:
        links_list.append(i.get_attribute("href"))
    #print(prices_list)
    try:
        print(settings.EXPORTS_ROOT)
        print(os.path.exists(settings.EXPORTS_ROOT))
        #minLen = min(len(names_list),len(prices_list),len(images_list),len(links_list))
        print(len(names_list))
        print(len(prices_list))
        print(len(images_list))
        print(len(links_list))
        prod_data = {
                "Product Name" : names_list,
                "Price" : prices_list,
                "Image Link": images_list,
                "Product Link" :links_list
            }
        print(settings.EXPORTS_ROOT)
        print(os.path.exists(settings.EXPORTS_ROOT))

        df = pd.DataFrame(prod_data)
        csv_file_path = os.path.join(settings.EXPORTS_ROOT, "amazon_data.csv")
        df.to_csv(csv_file_path,index = False,mode='a')
    except Exception as e:
        print("Error occured while storing to amazon_data.csv file")
    finally:
        driver.quit()
        product_data=zip(names_list,prices_list,images_list,links_list)
        data = list(product_data)
        return data
#print(ScrapAmazon("laptop"))