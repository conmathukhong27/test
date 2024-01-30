from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Set up Chrome options to run headless
def run(data_lake, driver):
  job_collection = data_lake['job_data']
  page_collection = data_lake['job_page']
  job_list = []
  pages = page_collection.find({'website': 'shopee'})
  for page in pages:
    # try:
    html_content = page['html_content']
    # Read page source
    driver.execute_script("document.children[0].innerHTML = {}".format(json.dumps(html_content)))

    # Wait for a few seconds to let the page load (adjust as needed)
    time.sleep(1)
    # Get the page source with the dynamically loaded content
    category = driver.find_element(By.CLASS_NAME, 'home-category-list')
    list_category_link = category.find_elements(By.TAG_NAME, 'a')
    i = 0
    for tr in list_category_link:
      if tr.get_attribute('href') is not None:
        link=tr.get_attribute('href')
        i += 1
        web='https://shopee.vn'
        page_index=0
        while page_index <50:
          page_index = page_index + 1
          page = f"?page={page_index}"
          web_link=web+link+page
          try:
            job_record = {
            'job_link': web_link,
            'website': page['website']
            }
            job_list.append(job_record)
          except:
            print(f"Failed to load web for page_index {page_index}")
            continue  # This ensures that even if an error occurs, the loop will continue for the next page_index
      print(job_record)
  for job in job_list:
    job_collection.update_one({'job_link': job['job_link']}, {'$set': job}, upsert=True)
  print('saved job data')


