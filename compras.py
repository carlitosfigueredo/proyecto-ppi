from calendar import c
from itertools import product
from click import confirm
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
driver.get('https://www.superseis.com.py/')

# BEGIN LOGIN
def login():
    for element in driver.find_elements(by=By.CLASS_NAME,value='btn-micuenta'):
        element.click()
    username = driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_topLoginView_ctrlCustomerLoginSmall_LoginFormSmall_UserName')
    username.send_keys("carlosalberto.figueredoquevedo@gmail.com")
    password =driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_topLoginView_ctrlCustomerLoginSmall_LoginFormSmall_Password')
    password.send_keys("HolaManola$$2020")
    submit = driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_topLoginView_ctrlCustomerLoginSmall_LoginFormSmall_LoginButton')
    submit.click()
#END LOGIN

#BEGIN SEARCH
def searchproducts(producto):
    searchs = driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ctl00_ctrlHeader_ctrlSearchBox_txtSearchTerms"]')
    searchs.send_keys(producto)
    sendform = driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ctl00_ctrlHeader_ctrlSearchBox_btnSearch"]')
    sendform.click()
#END SEARCH

def addCart(cantidad):
    sumarproducto = driver.find_element(by=By.CLASS_NAME,value='sumar')
    agregaralcarrito = driver.find_element(by=By.CLASS_NAME,value='productlistaddtocartbutton')
    for x in range(cantidad):
        sumarproducto.click()
    agregaralcarrito.click()

def viewCart():
    vercarrito = driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_MiniShoppingCartBox1_HyperLink1')
    vercarrito.click()

#DEFINO LA FUNCION ENVIAR FOTO
def sendFoto():
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S_%f")
    imagename = 'imagen'+date_time+'.png'
    mainpath = '/var/www/vhosts/selenium/'
    imgpath = 'img/'
    fullimgpath = mainpath+imgpath
    bottoken = '5332260147:AAH-q84fHpC0W15rKbyA3GlYd3KNkuYvm8c'
    chatid = '-528360114'
    #bottext = 'Shaggy'
    driver.save_screenshot(fullimgpath+imagename)
    fullimage = fullimgpath+imagename
    botimage = {'photo':open(fullimage,'rb')}
    send = requests.post("https://api.telegram.org/bot"+bottoken+"/sendPhoto?chat_id="+chatid,files=botimage)
    print(send.status_code)
    botimage.clear() 
    
#CHEQUEAR EL CARRITO AL INICIO Y VACIARLO
def checkCart():
    cantidadproductos = driver.find_elements(by=By.CLASS_NAME,value='cantidad')
    if cantidadproductos.text != '0':
        clearCart()

def clearCart():
    clearcart = driver.find_element(by=By.ID,value='vaciar-carrito')
    clearcart.click()
    confirmclear = driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_MiniShoppingCartBox1_btnVaciarCarrito')
    confirmclear.click()
    
#main
login()
#checkCart()
time.sleep(2)
producto = str("JUGO DE NARANJA")
cantidad = int(4)
time.sleep(10)
searchproducts(producto)
addCart(cantidad)
time.sleep(5)
viewCart()
time.sleep(100)
driver.quit()
