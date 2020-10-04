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
import numba as nb

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
        oled_font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\segoesc.ttf',13)  #14 is font size
    else:
        oled_font = ImageFont.truetype('simsun.ttc',14)
    msg = "LUCERO"
    w, h = oled_draw.textsize(msg)
    oled_draw.text(((OLED_SizeX-w)/2 - 10,0), msg, font=oled_font)
    oled_draw.text((OLED_SizeX - 12,7), "Hz")
    oled_font = ImageFont.truetype('simsun.ttc',11)
    msg = u"温度：\t99.9 ℃"
    oled_draw.text((15, OLED_SizeY - 47), msg, font=oled_font)
    msg = u"湿度：\t100 %"
    oled_draw.text((15, OLED_SizeY - 35), msg, font=oled_font)
    msg = u"气压：\t101.325 kPa"
    oled_draw.text((15, OLED_SizeY - 23), msg, font=oled_font)
    msg = u"VOC：\t100 %"
    oled_draw.text((15 + 4, OLED_SizeY - 11), msg, font=oled_font)
    while True:
        if platform.system() == "Windows":
            start = time.clock()
        else:
            start = time()
            
        # start1 = time.clock()
        oled_tmpbuf = (c_byte * (128*8))()   
        oled_lock.acquire()
        pixels = list(oled_img.getdata())
        oled_lock.release()
        convert(pixels, oled_tmpbuf)
        elapsed1 = (time.clock() - start)
        #logger.debug("%d ms", (int)(elapsed1*1000))
        OLED_Fill(oled_tmpbuf)

        if platform.system() == "Windows":
            elapsed = (time.clock() - start)
        else:
            elapsed = (time() - start)

        frq = 1 / elapsed
        frqs.append(frq)
        frq_avg = sum(frqs) / len(frqs)
        if len(frqs) > sum_size:
            frqs.pop(0)
        tmpstr = "{:f}".format(frq_avg)
        tmpstr = tmpstr[:4] + " Hz"
        #logger.debug("%02.1f Hz", frq_avg)
        oled_lock.acquire()
        oled_draw.rectangle((OLED_SizeX - 24,0,127,8),fill ='white')
        oled_draw.text((OLED_SizeX - 24,0), tmpstr)
        oled_lock.release()


def oled_thread_start():
    t1=Thread(target=oled_thread)
    t1.setDaemon(True)
    t1.start()
