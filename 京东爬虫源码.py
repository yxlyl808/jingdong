import json
from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
import time
s = ''

desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(executable_path='chromedriver.exe') #页面加载有可能超时，不需要等待加载完成

#driver = webdriver.Chrome()
#设置静默
'''chrome_options = Options()                                                   # 实例化Option对象
chrome_options.add_argument('--headless')                         # 把Chrome浏览器设置为静默模式
driver = webdriver.Chrome(options=chrome_options) '''        # 设置引擎为Chrome，在后台默默运行

driver.get('https://item.jd.com/100014562050.html')
time.sleep(3)
#driver.implicitly_wait(10)
driver.delete_all_cookies()
with open('jdcookies.txt', 'r') as f:
    cookies_list = json.load(f)
    for cookie in cookies_list:
        driver.add_cookie(cookie)
time.sleep(3)
driver.refresh()
time.sleep(3)

move = driver.find_element_by_xpath('//*[@id="area1"]/div[1]/b')
ActionChains(driver).move_to_element(move).perform() #鼠标悬停
tt2 = driver.find_element_by_xpath('//*[@id="area1"]/div[2]/div[1]/div[1]/b')
tt2.click() #点小箭头
t2 = driver.find_element_by_xpath('//*[@id="area1"]/div[2]/div[1]/div[2]/ul/li[1]/a') #武汉
t2.click()
t1 = driver.find_elements_by_class_name('summary-price-wrap')
for i in t1:
    s = s+i.text+'\n'
zeng1 = driver.find_elements_by_xpath('//*[@id="prom-gift"]/div/div/div/div/a')
for i in zeng1:
    s = s+i.get_attribute('title')+'\n'
time.sleep(3)

s = s+'-----------------------------------------------'+'\n'

move = driver.find_element_by_xpath('//*[@id="area1"]/div[1]/b')
ActionChains(driver).move_to_element(move).perform() #鼠标悬停
t2 = driver.find_element_by_xpath('//*[@id="area1"]/div[2]/div[1]/div[2]/ul/li[2]/a') #北京
t2.click()
t1 = driver.find_elements_by_class_name('summary-price-wrap')
for i in t1:
    s = s+i.text+'\n'
zeng2 = driver.find_elements_by_xpath('//*[@id="prom-gift"]/div/div/div/div/a')
for i in zeng2:
    s = s+i.get_attribute('title')+'\n'
time.sleep(3)
driver.close()
print(s)