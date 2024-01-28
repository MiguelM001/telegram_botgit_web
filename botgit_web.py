#!/usr/bin/env python
#
# -*- coding: utf-8 -*- 
#
# TITULO: BOT DE TELEGRAM PARA EL MONITOREO DE PORTALES WEB
#
# SUSCERTE: VENCERT
# DIRECCION DEL VENCERT
# AUTOR: MIGUEL MARQUEZ 
# CARACAS, ENERO DEL 2024
#
# botgit_web.py V1.0
#
#
import time
import telepot
import requests
import datetime
from PIL import Image
from selenium import webdriver
#import io

def enviarMensaje(bot, chat_id, message):
    bot.sendMessage(chat_id, message)

#def send_message_bold(bot, chat_id, message):
#    bot.sendMessage(chat_id, message, parse_mode="markdown")

def enviarFoto(bot, chat_id, photo_path):
    with open(photo_path, "rb") as file:
        bot.sendPhoto(chat_id, file)

def tiempoEstampa():
	tiempoActual= datetime.datetime.now()
	formato= tiempoActual.strftime("%d-%m-%Y %H:%M:%S")
	return str(formato)
	
def eliminarMensajes(bot, chat_id, eliminar):
    for i in range(0,len(eliminar)):
        bot.deleteMessage((chat_id, eliminar[i]))
    
def tiempoDeCarga(url):

        x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+str(url)+'&strategy=mobile'
        r = requests.get(x)
        final = r.json()
        try:
                urlfcp = final['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
                FCP = f'First Contentful Paint ~ {str(urlfcp)}'
                urlfi = final['lighthouseResult']['audits']['interactive']['displayValue']
                FI = f'{str(urlfi)}'
        except KeyError:
                mensaje=f'<KeyError> Una o más claves no encontradas https://vencert.suscerte.gob.ve.'

        try:
                mensaje=str("Portal: https://vencert.suscerte.gob.ve\nTiempo de carga: ")+FI

        except NameError:
                mensaje=f'<NameError> Fallo a causa de <KeyError> https://vencert.suscerte.gob.ve.'

        return mensaje

def capturarWeb(url):

        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(5)

        screenshot = driver.save_screenshot('captura.png')
        
        driver.quit()

def main():
    
    # lista 
    eliminar= list()

    # colocar url del portal a monitorear
    url="https://www.ejemplo.com"

    # contador
    cont=0
    
    # Obtener el token del bot de Telegram
    token = "<COLOCAR_TOKEN>"

    # Crear un bot de Telegram
    bot = telepot.Bot(token)

    # Obtener el ID del chat al que se enviará el mensaje
    chat_id = "<COLOCAR_ID_CHAT>"

    # Bucle infinito que envía el mensaje cada 10 minutos
    while True:
        capturarWeb(url)
        mensajeID1= enviarMensaje(bot, chat_id, tiempoEstampa())
        mensajeID2= enviarFoto(bot, chat_id, "captura.png")
        mensajeID3= enviarMensaje(bot, chat_id, tiempoDeCarga(url))
        #send_photo(bot, chat_id, "captura.png")
        #time.sleep(600)
        #print("prueba")
        # 432 veces son 3 dias
        #print("\n"+str(cont)+"\n")  
        eliminar.append(mensajeID1['message_id'])
        eliminar.append(mensajeID2['message_id'])
        eliminar.append(mensajeID3['message_id'])
        if cont == 432:
            #print(str(cont))
            #print("\nEntrooo")
            eliminarMensajes(bot, chat_id, eliminar)
            cont= 0
            eliminar.clear()
        
        cont= cont + 1 
        time.sleep(600)
if __name__ == "__main__":
    main()
