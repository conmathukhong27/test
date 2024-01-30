from bs4 import BeautifulSoup
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
def run(data_lake, driver):
  collection = data_lake['job_page']
  page_list = []
  url = f"https://shopee.vn"


# Khởi tạo trình duyệt
#   log_in= f"https://shopee.vn/user/login"

# # Mở trang đăng nhập Shopee
#   driver.get(log_in)

# # Tìm phần tử username theo attribute name
#   username_element = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div[2]/form/div[1]/div[1]/input')
#   password_element = driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div[2]/form/div[2]/div[1]/input')
#   time.sleep(5)
#   username_element.send_keys("")
#   time.sleep(5)
#   password_element.send_keys("")  
# # Submit để đăng nhập
#   time.sleep(5)
#   password_element.send_keys(Keys.RETURN)
#   time.sleep(5)
  driver.get(url)
  soup = BeautifulSoup(driver.page_source, "html.parser")
  soup_string = str(soup)
    
  # Get the page source with the dynamically loaded content
  page_source = driver.page_source
  page_list.append({
      'html_content': soup_string,
      'website': 'shopee',
      'page_link': url,
      'date': datetime.now()
    })
  print(page_list)
  for page in page_list:
    collection.update_one({'page_link': page['page_link']}, {'$set': page}, upsert=True)
  # save page_source into database
  print('saved search job pages')
