import threading
from threading import Lock,Thread
import time,os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
from ctypes import *
import time
import platform
from oled import *
#import numba as nb
from bme680 import *
import globalvar


oled_lock = Lock()

OLED_SizeX = 128
OLED_SizeY = 64
oled_img = Image.new("1",(OLED_SizeX, OLED_SizeY),"white")
oled_draw = ImageDraw.Draw(oled_img)

#@nb.jit()
def convert(pixels, buf):    
    for y in range(0, 64):
        for x in range(0, 128):
            pixel = pixels[x + y*128]
            if pixel == 0 :
                pixel = 1
            else:
                pixel = 0
            pixel = pixel << (y % 8)
            index = int(int(y / 8) * OLED_SizeX + x)
            buf[index] |= pixel

def oled_thread():
    frqs = []
    frq_avg = 0
    sum_size = 10
    
    if platform.system() == "Windows":
        oled_font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\segoesc.ttf',13)  #14 is font size  # simsun.ttc
    elif platform.system() == "Linux":
        oled_font = ImageFont.truetype('NotoSansCJK-Regular.ttc',13) # 'fc-list :lang=zh' command look for Chinese fonts
    elif platform.system() == "Darwin":
        oled_font = ImageFont.truetype('/System/Library/AssetsV2/com_apple_MobileAsset_Font6/00e58c0676b9e589e9309dbca4b795bbba3b5420.asset/AssetData/Kaiti.ttc',13) # brew install fontconfig than 'fc-list :lang=zh' command look for Chinese fonts
    else:
        oled_font = ImageFont.truetype('simsun.ttc', 13)
    msg = "LUCERO"
    w, h = oled_draw.textsize(msg)
    oled_draw.text(((OLED_SizeX-w)/2 - 10,0), msg, font=oled_font)
    oled_draw.text((OLED_SizeX - 12,7), "Hz")
    if platform.system() == "Windows":
        oled_font = ImageFont.truetype('simsun.ttc',11)
        xstart = 10
    elif platform.system() == "Linux":
        oled_font = ImageFont.truetype('NotoSansCJK-Regular.ttc',9)
        xstart = 25
    elif platform.system() == "Darwin":
        oled_font = ImageFont.truetype('/System/Library/AssetsV2/com_apple_MobileAsset_Font6/ec2979c8550757993101e27b30b2b89cb45917fc.asset/AssetData/Yuanti.ttc',10)
        xstart = 15
    else:
        xstart = 15
    while True:
        start = time.perf_counter()
            
        # start1 = time.perf_counter()
        oled_tmpbuf = (c_byte * (128*8))()   
        oled_lock.acquire()
        pixels = list(oled_img.getdata())
        oled_lock.release()
        convert(pixels, oled_tmpbuf)
        elapsed1 = (time.perf_counter() - start)
        #logger.debug("%d ms", (int)(elapsed1*1000))
        OLED_Fill(oled_tmpbuf)

        elapsed = (time.perf_counter() - start)

        frq = 1 / elapsed
        frqs.append(frq)
        frq_avg = sum(frqs) / len(frqs)
        if len(frqs) > sum_size:
            frqs.pop(0)
        tmpstr = "{:f}".format(frq_avg)
        tmpstr = tmpstr[:4]
        #logger.debug("%02.1f Hz", frq_avg)
        oled_lock.acquire()
        oled_draw.rectangle((OLED_SizeX - 24,0,127,8),fill ='white') #frequency
        oled_draw.text((OLED_SizeX - 24,0), tmpstr)        
        BME680_lock.acquire()
        temp = globalvar.get_value('BME680_Temperature')
        hum =  globalvar.get_value('BME680_Humidity')
        press =  globalvar.get_value('BME680_Pressure')
        aqi =  globalvar.get_value('BME680_AQI')
        BME680_lock.release()  
        if temp != None and hum != None and press != None and aqi != None:
            oled_draw.rectangle((0, 18,127,63),fill ='white') # data region
            msg = u"温度：  {:.2f} ℃".format(temp)
            oled_draw.text((xstart, OLED_SizeY - 47), msg, font=oled_font)
            msg = u"湿度：  {:.2f} % RH".format(hum)
            oled_draw.text((xstart, OLED_SizeY - 35), msg, font=oled_font)
            msg = u"气压：  {:.3f} kPa".format(press)
            oled_draw.text((xstart, OLED_SizeY - 23), msg, font=oled_font)
            msg = u"AQI：  {:.2f}".format(aqi)
            # 根据《环境空气质量指数（AQI）技术规定（试行）》（HJ 633—2012）规定
            if aqi == 0:
                msg += ' Burn in'
            elif aqi <= 50:
                msg += u'  优'
            elif aqi <= 100:
                msg += u'  良'
            elif aqi <= 150:
                msg += u' 轻度'
            elif aqi <= 200:
                msg += u' 中度'
            elif aqi <= 300:
                msg += u' 重度'
            else:
                msg += u' 严重'
            oled_draw.text((xstart + 4, OLED_SizeY - 11), msg, font=oled_font)
        oled_lock.release()


def oled_thread_start():
    t1=Thread(target=oled_thread)
    t1.setDaemon(True)
    t1.start()
