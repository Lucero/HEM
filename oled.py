from device import *
from usb2iic import *
from logger import *

IICIndex_OLED = 2
IICAddr_OLED = 0x3C

def OLED_Init():
    logger.info ('Initialize i2c')
    IICConfig = IIC_CONFIG()
    IICConfig.ClockSpeed = 400000
    IICConfig.Master = 1
    IICConfig.AddrBits = 7
    IICConfig.EnablePu = 1
    ret = IIC_Init(DevHandles[DevIndex],IICIndex_OLED,byref(IICConfig));
    if ret != IIC_SUCCESS:
        logger.critical("Initialize iic faild!")
        exit()
    else:
        logger.info("Initialize iic sunccess!")
        
    SlaveAddr = (c_ushort * 128)()
    SlaveAddrNum = IIC_GetSlaveAddr(DevHandles[DevIndex],IICIndex_OLED,byref(SlaveAddr))
    if SlaveAddrNum <= 0:
        logger.critical("Get iic address faild!")
        exit()
    else:
        logger.info("Get iic address sunccess!")
        OledConnected = False
        for i in range(0,SlaveAddrNum):
            if (SlaveAddr[i] == IICAddr_OLED):
                OledConnected = True
                logger.info('OLED 0x%02X Connected', SlaveAddr[i])
        if OledConnected == False:
            logger.critical("OLED not connect!")
            exit()

    
    logger.info ('OLED init')
    WriteBuffer = (c_byte * 9)()
    WriteBuffer[0] = 0x00 # command
    for i in range(0, 27):
        if i == 0:
            WriteBuffer[1] = 0xAE # display off
        elif i == 1:
            WriteBuffer[1] = 0x00 # set low column address
        elif i == 2:
            WriteBuffer[1] = 0x10 # set high column address
        elif i == 3:
            WriteBuffer[1] = 0x40 # set start line address
        elif i == 4:
            WriteBuffer[1] = 0xB0 # set page address
        elif i == 5:
            WriteBuffer[1] = 0x81 # contract control
        elif i == 6:
            WriteBuffer[1] = 0xFF # 128 
        elif i == 7:
            WriteBuffer[1] = 0xA1 # set segment remap 
        elif i == 8:
            WriteBuffer[1] = 0xA6 # normal / reverse
        elif i == 9:
            WriteBuffer[1] = 0xA8 # set multiplex ratio(1 to 64)
        elif i == 10:
            WriteBuffer[1] = 0x3F # 1/32 duty
        elif i == 11:
            WriteBuffer[1] = 0xC8 # Com scan direction
        elif i == 12:
            WriteBuffer[1] = 0xD3 # et display offset
        elif i == 13:
            WriteBuffer[1] = 0x00 #
        elif i == 14:
            WriteBuffer[1] = 0xD5 # set osc division
        elif i == 15:
            WriteBuffer[1] = 0x80 #
        elif i == 16:
            WriteBuffer[1] = 0xD8 # set area color mode off
        elif i == 17:
            WriteBuffer[1] = 0x05 # 
        elif i == 18:
            WriteBuffer[1] = 0xD9 # Set Pre-Charge Period
        elif i == 19:
            WriteBuffer[1] = 0xF1 # 
        elif i == 20:
            WriteBuffer[1] = 0xDA # set com pin configuartion
        elif i == 21:
            WriteBuffer[1] = 0x12 # 
        elif i == 22:
            WriteBuffer[1] = 0xDB # set Vcomh
        elif i == 23:
            WriteBuffer[1] = 0x30 # 
        elif i == 24:
            WriteBuffer[1] = 0x8D # set charge pump enable
        elif i == 25:
            WriteBuffer[1] = 0x14 #
        elif i == 26:
            WriteBuffer[1] = 0xAF # turn on oled panel
        ret = IIC_WriteBytes(DevHandles[DevIndex], IICIndex_OLED, IICAddr_OLED, WriteBuffer, 2, 1000)
        if(ret != IIC_SUCCESS):
            logger.critical("OLED init cmd %d failed!", i)
            exit()
    OLED_Clear()

def OLED_Fill(data):
    #logger.info ('OLED Fill')
    WriteBuffer = (c_byte * 256)()
    for i in range(0, 8):
        WriteBuffer[0] = 0x00 # command
        for j in range(0, 3):
            if j == 0:
                WriteBuffer[1] = 0xB0 + i # 设置页地址（0~7）
            elif j == 1:
                WriteBuffer[1] = 0x00 # set low column address
            elif j == 2:
                WriteBuffer[1] = 0x10 # set high column address
            ret = IIC_WriteBytes(DevHandles[DevIndex], IICIndex_OLED, IICAddr_OLED, WriteBuffer, 2, 1000)
            if(ret != IIC_SUCCESS):
                logger.error("OLED Clear cmd %d.%d failed!", i, j)
        WriteBuffer[0] = 0x40 # command
        for j in range(0, 128):
            WriteBuffer[1 + j] = data[i * 128 + j]
        ret = IIC_WriteBytes(DevHandles[DevIndex], IICIndex_OLED, IICAddr_OLED, WriteBuffer, 129, 1000)
        if(ret != IIC_SUCCESS):
            logger.error("OLED Fill data %d.%d failed!", i, j)

def OLED_Clear():
    WriteBuffer = (c_byte * (128*8))()
    for i in range(0, 128*8):
        WriteBuffer[i] = 0x0
    OLED_Fill(WriteBuffer)

    














