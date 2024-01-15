#!/usr/bin/python
# -*- coding: utf-8 -*-

## ESSID/reboot(/power on) Raspberry Pi con comandi GPIO pushbutton

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time
# import subprocess
import signal
import os
# from time import sleep


## pulsante collegato al pin GPIO raspberry pi zero W
pin_37 = 37

## se il pulsante è premuto per almeno questo tempo allora verrà eseguito il PRIMO comando, altrimenti  se inferiore verrà eseguito il SECONDO comando
restartMinSeconds = 4

## button debounce time in seconds
debounceSeconds = 0.01

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPressedTime = None


def buttonStateChanged(pin_37):
    global buttonPressedTime

    if not (GPIO.input(pin_37)):
        ## button is down
        if buttonPressedTime is None:
            buttonPressedTime = datetime.now()
    else:
        ## button is up
        if buttonPressedTime is not None:
            elapsed = (datetime.now() - buttonPressedTime).total_seconds()
            buttonPressedTime = None
            if elapsed >= restartMinSeconds:
                ## timeout button pressed>=shutdownMinSeconds -----> eseguo PRIMO COMANDO
                #call(['shutdown', '-h', 'now'], shell=False)
                print ("---<RESET>---")
                #call(['shutdown', '-r', 'now'], shell=False)
                #os.system("/home/pi/SNAP7/button/set_as_ap.sh")
                os.system("/home/pi/MODBUS/button/set_as_ap.sh")
            elif elapsed >= debounceSeconds:
                ## timeout button pressed<shutdownMinSeconds -----> eseguo SECONDO comando
                #call(['shutdown', '-r', 'now'], shell=False)
                #subprocess.Popen("/home/pi/button/essid.sh", shell=True, preexec_fn=os.setsid)
                #call(["/home/pi/button/essid.sh"], shell=False)
                #call(["/home/pi/MODBUS/button/essid.sh"], shell=False)
                #call(["/home/pi/MODBUS/button/restartAP.sh"], shell=False)
                print ("<buttonState=pressed>")


## BUTTON PUSH ----> Scateno EVENTO: cambio di stato PIN [high1=1]
GPIO.add_event_detect(pin_37, GPIO.BOTH, callback=buttonStateChanged)

while True:
    ##DELAY: ** ---riduco utilizzo CPU usage--- **
    time.sleep(0.5)
