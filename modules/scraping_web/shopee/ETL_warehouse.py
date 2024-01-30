from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json
from modules.utils import convert_string_to_date
from datetime import datetime, timedelta

def run(data_lake, data_warehouse, driver):
  cursor = data_warehouse.cursor()
  collection = data_lake['job_page']
  job_records = collection.find({'website': 'shopee'}, no_cursor_timeout=True).batch_size(10)
  for page in job_records:
    html_content = page['html_content']
    # Read page source
    driver.execute_script("document.children[0].innerHTML = {}".format(json.dumps(html_content)))
    # Wait for a few seconds to let the page load (adjust as needed)
    time.sleep(15)
    # Get the page source with the dynamically loaded content
    product = driver.find_element(By.CLASS_NAME, 'uXYBTq')
    list_product= product.find_elements(By.TAG_NAME, 'a')
    i = 0
    for tr in list_product:
      if tr.get_attribute('href') is not None:
        i+=1
        product_url = tr.get_attribute('href')
        prouduct_name = tr.find_element(By.CLASS_NAME, 'DgXDzJ rolr6k Zvjf4O').text
        product_price= tr.find_element(By.CLASS_NAME, 'cA9TT+').text
        history_sold= tr.find_element(By.CLASS_NAME, 'OwmBnn eumuJJ').text 
        product_rating =[]
        product_rate=tr.find_elements(By.CLASS_NAME, 'shopee-rating-stars__star-wrapper')
        for rate in product_rate:
          rate_1=rate.find_element(By.CLASS_NAME, 'shopee-rating-stars__lit')
          if rate_1.get_attribute('style') is not None:
            product_rating.append(rate_1.get_attribute('style'))
        job_wh_record = {
          'product_url': product_url,
          'prouduct_name':prouduct_name,
          'product_price':product_price,
          'history_sold':history_sold,
          'product_rating':product_rating
        }
        print(job_wh_record)
        data_to_upsert = [(str(job_wh_record['product_url']), str(job_wh_record['prouduct_name']), str(job_wh_record['product_price']),str(job_wh_record['history_sold']),str(job_wh_record['product_rating']))]
        upsert_query = '''
        INSERT INTO job_table (product_url, prouduct_name, product_price, history_sold, product_rating)
        VALUES %s
        SET product_url = EXCLUDED.product_url,
            prouduct_name = EXCLUDED.prouduct_name,
            product_price= EXCLUDED.product_price,
            history_sold= EXCLUDED.history_sold,
            product_rating= EXCLUDED.product_rating;
        '''
        cursor.execute(upsert_query, data_to_upsert)
        data_warehouse.commit()
        # job_collection.update_one({'job_link': job_wh_record['job_link']}, {'$set': {'ETL': True}}, upsert=True)
  
