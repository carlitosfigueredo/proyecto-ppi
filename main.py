from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, signal
from cgitb import text
from email import message
from http.server import executable
from lib2to3.pgen2 import driver
import time
from selenium import webdriver
from PIL import Image
import requests
from datetime import datetime

driver = webdriver.Chrome('/var/www/vhosts/selenium/chromedriver')
driver.set_window_position(2000,0)
driver.maximize_window()
driver.get('https://www.unida.edu.py')
mainpath = '/var/www/vhosts/selenium/'
imgpath = 'img/'
fullimgpath = mainpath+imgpath
now = datetime.now()
date_time = now.strftime("%m_%d_%Y_%H_%M_%S_%f")
imagename = 'imagen'+date_time+'.png'
#print('imagen name: '+imagename)
driver.save_screenshot(fullimgpath+imagename)
time.sleep(4)

for element in driver.find_elements(by=By.CLASS_NAME,value='menu-link'):
    if element.text == 'E-Class':
        element.click()
for element in driver.find_elements(by=By.CLASS_NAME,value='hero_box'):
    if element.text == 'Estudiantes':
        element.click()




bottoken = '5332260147:AAH-q84fHpC0W15rKbyA3GlYd3KNkuYvm8c'
chatid = '-528360114'
bottext = 'Shaggy'
fullimage = fullimgpath+imagename
botimage = {'photo':open(fullimage,'rb')}

send = requests.post("https://api.telegram.org/bot"+bottoken+"/sendPhoto?chat_id="+chatid,files=botimage)
print(send.status_code)
botimage.clear()
time.sleep(5)
driver.quit()
