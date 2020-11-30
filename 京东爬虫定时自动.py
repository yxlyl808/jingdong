from email.utils import parseaddr, formataddr
import smtplib
import schedule
from email.mime.text import MIMEText
from email.header import Header
import json
from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
import time

def get_w():
    s = ''

    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(executable_path='chromedriver.exe')  # 页面加载有可能超时，不需要等待加载完成

    # driver = webdriver.Chrome()

    driver.get('https://item.jd.com/100014562050.html')
    time.sleep(3)
    # driver.implicitly_wait(10)
    driver.delete_all_cookies()
    with open('jdcookies.txt', 'r') as f:
        cookies_list = json.load(f)
        for cookie in cookies_list:
            driver.add_cookie(cookie)
    time.sleep(3)
    driver.refresh()
    time.sleep(3)

    move = driver.find_element_by_xpath('//*[@id="area1"]/div[1]/b')
    ActionChains(driver).move_to_element(move).perform()  # 鼠标悬停
    tt2 = driver.find_element_by_xpath('//*[@id="area1"]/div[2]/div[1]/div[1]/b')
    tt2.click()  # 点小箭头
    t2 = driver.find_element_by_xpath('//*[@id="area1"]/div[2]/div[1]/div[2]/ul/li[1]/a')  # 武汉
    t2.click()
    time.sleep(5)
    t1 = driver.find_elements_by_class_name('summary-price-wrap')
    for i in t1:
        s = s + i.text + '\n'
    zeng1 = driver.find_elements_by_xpath('//*[@id="prom-gift"]/div/div/div/div/a')
    for i in zeng1:
        s = s + i.get_attribute('title') + '\n'
    time.sleep(3)

    s = s + '-----------------------------------------------' + '\n'

    move = driver.find_element_by_xpath('//*[@id="area1"]/div[1]/b')
    ActionChains(driver).move_to_element(move).perform()  # 鼠标悬停
    t2 = driver.find_element_by_xpath('//*[@id="area1"]/div[2]/div[1]/div[2]/ul/li[2]/a')  # 北京
    t2.click()
    time.sleep(5)
    t1 = driver.find_elements_by_class_name('summary-price-wrap')
    for i in t1:
        s = s + i.text + '\n'
    zeng2 = driver.find_elements_by_xpath('//*[@id="prom-gift"]/div/div/div/div/a')
    for i in zeng2:
        s = s + i.get_attribute('title') + '\n'
    time.sleep(3)
    driver.close()
    return s
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def send_email(s, sender, pwd, recevier):
    mailhost='smtp.qq.com'
    qqmail = smtplib.SMTP_SSL(mailhost, 465)
    qqmail.login(sender, pwd)
    content = '当前时间：'+time.strftime('%H:%M:%S',time.localtime(time.time()))+'\n'+s
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = formataddr((Header(u'10至尊，武汉和北京', 'utf-8').encode(), sender))
    message['To'] = formataddr((Header(u'lyl', 'utf-8').encode(), recevier))
    message['Subject'] = Header(u'京东价格监控', 'utf-8').encode()
    try:
        qqmail.sendmail(sender, recevier, message.as_string())
        qqmail.quit()
        return True
    except:
        return False
def job():
    print('开始一次发送任务')
    s = get_w()
    IsSuccess = send_email(s, sender, pwd, recevier) # 这里需要设置发件人的账号密码以及收件人的账号
    while IsSuccess is False:
        print("邮件发送失败，正在尝试重新发送")# sender是自己的邮箱号，pwd是邮箱密码,recevier是接收邮箱的账号，这三个变量均为字符串类型，需要自己手动添加
        IsSuccess = send_email(s, sender, pwd, recevier)
    print('任务完成')


sender = '1928582659@qq.com'
pwd = ' '
recevier = 'yxlyl808@126.com'

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
