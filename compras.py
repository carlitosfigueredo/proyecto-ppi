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
from variablesCliente import *
from listaDeCompra import *
import json
#Inicializacion del driver para el scrapping
driver = webdriver.Chrome('/var/www/vhosts/selenium/chromedriver')
driver.set_window_position(2000,0)
driver.maximize_window()
driver.get('https://www.superseis.com.py/')

# Funcion de inicio de sesion
def login():
    for element in driver.find_elements(by=By.CLASS_NAME,value='btn-micuenta'):
        element.click()
    username = driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_topLoginView_ctrlCustomerLoginSmall_LoginFormSmall_UserName')
    username.send_keys(usuarioSuper6)
    password =driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_topLoginView_ctrlCustomerLoginSmall_LoginFormSmall_Password')
    password.send_keys(passwordSuper6)
    submit = driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_topLoginView_ctrlCustomerLoginSmall_LoginFormSmall_LoginButton')
    submit.click()
# Fin de la funcion


#CHEQUEAR EL CARRITO AL INICIO Y VACIARLO
def checkCart():
    cantidadproductos = driver.find_element(by=By.XPATH,value='//*[@id="ver_carro"]/div/div[1]/div/strong').text
    if cantidadproductos != '0':
        clearCart()
    else:
        print("Carrito VACIO")
        return
# Fin de la funcion

def clearCart():
    clickCart = driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_MiniShoppingCartBox1_botonera')
    clickCart.click()
    driver.implicitly_wait(5)
    clearcart = driver.find_element(by=By.XPATH,value='//*[@id="productos"]/div[3]/div[1]')
    clearcart.click()
    driver.implicitly_wait(5)
    confirmclear = driver.find_element(by=By.NAME,value='ctl00$ctl00$ctrlHeader$MiniShoppingCartBox1$btnVaciarCarrito')
    confirmclear.click()
    print("El carrito ha sido vaciado")

# Fin de la funcion
def searchproducts():
    data = json.loads(listaCompra)
    for item in data:
        productoComprar = item["producto"]
        cantidadComprar = int(item["cantidad"])
        print(productoComprar)
        print(cantidadComprar)
        searchs = driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ctl00_ctrlHeader_ctrlSearchBox_txtSearchTerms"]')
        searchs.send_keys(productoComprar)
        sendform = driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ctl00_ctrlHeader_ctrlSearchBox_btnSearch"]')
        sendform.click()
        addCart(cantidadComprar)
# Fin de la funcion

def addCart(cantidadComprar):
    sumarproducto = driver.find_element(by=By.CLASS_NAME,value='sumar')
    agregaralcarrito = driver.find_element(by=By.CLASS_NAME,value='productlistaddtocartbutton')
    for x in range(cantidadComprar):
        sumarproducto.click()
    agregaralcarrito.click()
    sendFoto()
    
# Fin de la funcion

def viewCart():
    vercarrito = driver.find_element(by=By.ID,value='ctl00_ctl00_ctrlHeader_MiniShoppingCartBox1_HyperLink1')
    vercarrito.click()
# Fin de la funcion

#DEFINO LA FUNCION ENVIAR FOTO 
def sendFoto():
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S_%f")
    imagename = 'imagen'+date_time+'.png'
    mainpath = '/var/www/vhosts/selenium/'
    imgpath = 'img/'
    fullimgpath = mainpath+imgpath
    bottoken = '5399266757:AAFaDpCYo2nYRqlE2Kng9ZQv3PYE1ACXImk'
    chatid = chatIdTelegramCliente
    driver.save_screenshot(fullimgpath+imagename)
    fullimage = fullimgpath+imagename
    botimage = {'photo':open(fullimage,'rb')}
    send = requests.post("https://api.telegram.org/bot"+bottoken+"/sendPhoto?chat_id="+chatid,files=botimage)
    print(send)
    print(send.status_code)
    botimage.clear() 
# Fin de la funcion  
    
def sendFinalMessage():
    subtototal = driver.find_element(by=By.ID,value='ctl00_ctl00_cph1_cph1_OrderSummaryControl_ctrlOrderTotals_lblSubTotalAmount').text
    subtotalTexto = "El subtotal de su compra es: "+subtototal
    envio = driver.find_element(by=By.ID,value='ctl00_ctl00_cph1_cph1_OrderSummaryControl_ctrlOrderTotals_lblShippingAmount').text
    envioTexto = "El Costo de envío de su compra será de: "+envio
    total = driver.find_element(by=By.ID,value='ctl00_ctl00_cph1_cph1_OrderSummaryControl_ctrlOrderTotals_lblTotalAmount').text
    totalTexto = "El Total General de su compra será de: "+total
    bottoken = '5399266757:AAFaDpCYo2nYRqlE2Kng9ZQv3PYE1ACXImk'
    chatid = chatIdTelegramCliente
    sendSaludo = requests.post("https://api.telegram.org/bot"+bottoken+"/sendMessage?chat_id="+chatid+"&text="+mensajeCarrito)
    sendSubtotal = requests.post("https://api.telegram.org/bot"+bottoken+"/sendMessage?chat_id="+chatid+"&text="+subtotalTexto)
    sendCostoEnvio = requests.post("https://api.telegram.org/bot"+bottoken+"/sendMessage?chat_id="+chatid+"&text="+envioTexto)
    sendTotal = requests.post("https://api.telegram.org/bot"+bottoken+"/sendMessage?chat_id="+chatid+"&text="+totalTexto)
    # Prints de ejecucion a modo de log
    print(sendSaludo)
    print(sendSaludo.status_code)
    print(sendSubtotal)
    print(sendSubtotal.status_code)
    print(sendCostoEnvio)
    print(sendCostoEnvio.status_code)
    print(sendTotal)
    print(sendTotal.status_code)
# Fin de la funcion

#Ejecucion Principal
login()
time.sleep(5)
sendFoto()
checkCart()
sendFoto()
time.sleep(10)
searchproducts()
sendFoto()
time.sleep(5)
viewCart()
sendFinalMessage()
sendFoto()
time.sleep(500)
driver.quit()
