#!/usr/bin/python3
from re import I
import sys
import csv
import time
import datetime
from dateutil.rrule import rrule, MONTHLY
import numpy as np
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support.select import Select

# here is the link for splitting ht estring https://docs.python.org/3.3/library/stdtypes.html?highlight=split
class Book:
  def __init__(self, headless, chrome=False):
    opt = Options()
    opt.add_argument("--window-size=1920,1080")
    opt.add_argument("--incognito")
    if headless:
        opt.add_argument('--headless')
    if chrome:
      self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=opt)
    
  def get_bookeo(self):
    self.driver.get('https://www.bookeo.com/')

    print(f'Selenium runnning at session {self.driver.session_id}') 
  
  def close_crawler(self):
    self.driver.close()

  def sign_in(self, _username, _password):
    click_to_sign_in = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'body > header > div.header-wrap.container > div > div > a:nth-child(1)'))).click()
    email_address = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="loginBk"]/form/div/table/tbody/tr[1]/td/input'))).send_keys(_username)
    password = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(_password)         
    sign_in = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR,'#login'))).click()

  def move_to_marketing(self):
    marketing = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[1]/div[2]/div[4]'))).click()
    stats_and_charts = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, \
                       '.bigsettingsTable > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > div:nth-child(6)'))).click()    
    history = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div[2]'))).click()

  def calender_distance(self, d1_month, d1_year, d2_month, d2_year):
    months = {j:i+1 for i,j in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                          'August', 'September', 'October', 'November', 'December'])}
    strt_dt = datetime.date(d1_year, months[d1_month], 1)
    end_dt = datetime.date(d2_year, months[d2_month], 1)
    months = dict((v,k) for k,v in months.items())
    return [[months[dt.month], dt.year] for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]

  def gac_month_to_month(self, d1_month, d1_year, d2_month, d2_year):
    domain = self.calender_distance(d1_month, d1_year, d2_month, d2_year)
    urls = []
    for i in range(1, len(domain)):
      select = Select(self.driver.find_element(By.NAME, 'month1'))     
      s1 = domain[i-1][0]+' '+str(domain[i-1][1])
      s2 = domain[i][0]+' '+str(domain[i][1])
      print(f'Iteration {i} out of {len(domain)}')
      select.select_by_visible_text(domain[i-1][0]+' '+str(domain[i-1][1]))
      select2 = Select(self.driver.find_element(By.NAME, 'month2'))
      select2.select_by_visible_text(domain[i][0]+' '+str(domain[i][1]))
      refresh = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.ui3smallbtn'))).click()
      time.sleep(3)
      urls.append(self.driver.page_source)
    df = pd.concat([pd.concat(pd.read_html(url, header=0), axis=0) for url in urls], axis=1)
    return df.to_csv('Month_to_Month_comparison.csv', index=False)

  def gac_yearly(self, month, start, stop, verbose=False):
    domain = [month+' '+str(i) for i in range(start, stop+1)]
    urls = []
    months = []
    for i in range(1, len(domain)):
      select = Select(self.driver.find_element(By.NAME, 'month1')) 
      select.select_by_visible_text(domain[i-1])
      select2 = Select(self.driver.find_element(By.NAME, 'month2'))
      print(f'Iteration {i} out of {len(domain)}')
      select2.select_by_visible_text(domain[i])
      dates = domain[i-1] + domain[i]
      refresh = WebDriverWait(self.driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.ui3smallbtn'))).click()      
      if verbose:
        time.sleep(3)
      urls.append(self.driver.page_source)
    df = pd.concat([pd.concat(pd.read_html(url, header=0), axis=0) for url in urls], axis=1)
    return df.to_csv('Yearly_comparison.csv', index=False)
      

"""
b = Book(1, 1)
b.get_bookeo()
#need to pass signin informationt to run this in main

b.move_to_marketing()
#b.get_all_content('January', 2018, 2022)
#b.gac_yearly('January', 2018, 2022)
b.revenue_comparsion('January', 2018, 'June', 2022)
b.close_crawler()
"""





