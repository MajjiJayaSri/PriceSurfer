from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
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
    names=driver.find_elements(By.XPATH,"//h2[contains(@class,'a-size-medium a-spacing-none a-color-base a-text-normal')]")
    prices=driver.find_elements(By.XPATH,"//span[contains(@data-a-size,'xl')]//span[@class='a-offscreen']")
    images = driver.find_elements(By.XPATH, "//div[contains(@class,'a-section aok-relative s-image-fixed-height')]/img")
    links=driver.find_elements(By.XPATH,"//a[contains(@class, 'clamp-2')]")
    #driver.quit()
    print(prices)
    names_list=[]
    prices_list=[]
    images_list=[]
    links_list=[]
    for i in names:
        names_list.append(i.text)
        
    # for i in prices:
    #     print(i.text)
    #     prices_list.append(i.text)
    prices_list = []

    for price in prices:
        driver.execute_script("arguments[0].scrollIntoView(true);", price)
        price_text = price.get_attribute("innerText").strip()  # or use price.text
        if price_text:
            prices_list.append(price_text)
        else:
            print("Empty text for element:", price)

    print(prices_list)

    for i in images:
        images_list.append(i.get_attribute("src"))
        
    for i in links:
        links_list.append(i.get_attribute("href"))
    print(prices_list)
    
    product_data=zip(names_list,prices_list,images_list,links_list)
    data = list(product_data)
    return data
#print(ScrapAmazon("laptop"))