#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'京东商家后台预警商品自动处理工具'
__author__ = 'Zhang Minghao'

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

#修改为自己的chrome浏览器文件路径
chrome_location = r"D:\Program Files\Chrome\Chrome\chrome.exe"
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=3')
chrome_options.binary_location = chrome_location
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://shop.jd.com/')
input('等待手动登陆，登陆完成后按回车键继续！')
time.sleep(1)
data_xpath = '/html/body/div[2]/div/div[3]/div[2]/div/div/div[4]/table/tbody'
next_page_xpath = '//a[contains(text(),"下一页")]'
handle = driver.current_window_handle

def run():
    driver.switch_to.window(handle)
    data = driver.find_element_by_xpath(data_xpath)
    list = data.find_elements_by_tag_name('tr')
    for i in list:
        try:
            i.find_element_by_tag_name('span').click()
            time.sleep(0.5)
            if len(driver.window_handles) != 1:
                #切换到在售商品管理页面
                driver.switch_to.window(driver.window_handles[-1])
                wait_for_load()
                driver.find_element_by_id('top_selectAll').click()
                time.sleep(0.5)
                driver.find_element_by_id('top_bt_down').click()
                time.sleep(1)
                dig_confirm = driver.switch_to.alert
                dig_confirm.accept()
                time.sleep(1)
                driver.close()
                print('商品下架成功')
                #返回商品预警列表
                driver.switch_to.window(handle)
                i.find_element_by_tag_name('span').click()
                time.sleep(0.5)
                driver.switch_to.window(driver.window_handles[-1])
                #切换到待售商品管理页面
                wait_for_load()
                driver.find_element_by_id('top_selectAll').click()
                time.sleep(0.5)
                driver.find_element_by_id('top_bt_del').click()
                time.sleep(1)
                driver.find_element_by_xpath('//a[contains(text(),"确定")]').click()
                time.sleep(1)
                driver.close()
                print('商品删除成功')
                driver.switch_to.window(handle)
                #input('商品处理完成后按回车继续！')
            else:
                alert_status = 0
                while alert_status < 3:
                    try:
                        driver.switch_to_alert().accept()
                        break
                    except:
                        alert_status += 1
                        time.sleep(1)
                        continue
        except:
            continue
    driver.find_element_by_xpath(next_page_xpath).click()
    time.sleep(1)
    
    
def wait_for_load():
    wait_for_load_count = 0
    while wait_for_load_count < 3:
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='top_selectAll']")))
            print('商品管理页面载入成功')
        except:
            wait_for_load_count += 1
            print('等待商品管理页面载入')
            continue
        break

while 1:
    driver.get('https://legal.shop.jd.com/venderWarning/attributesMutex.action')
    try:
        while 1:
            run()
    except exceptions.WebDriverException:
        print('浏览器窗口意外关闭或登陆失效，请重新运行程序')
        break
    except exceptions.NoSuchWindowException:
        driver.switch_to.window(driver.window_handles[-1])
        continue
    except:
        print('出现未知错误，请重新运行程序')
        break
