from ctypes import *
from device import *
from oled import *
from sensor import *
from time import sleep
from logger import *
from oled_thread import *

def main():
    device_open()
    Sensor_Init()
    OLED_Init()
    oled_thread_start()
    
    while True:
        time.sleep(1)
    


if __name__ == '__main__': 
    main()
