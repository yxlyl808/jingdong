from selenium import webdriver
import time
import json
driver = webdriver.Chrome()
driver.get('https://item.jd.com/100014562050.html')
time.sleep(60)
with open('jdcookies.txt','w') as f:
    f.write(json.dumps(driver.get_cookies()))
driver.close()
