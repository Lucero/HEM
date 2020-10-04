from device import *
from usb2iic import *
from logger import *

IICIndex_Sensor = 0
IICAddr_Sensor = 0x77

def Sensor_Init():
    logger.info ('Sensor init')

    logger.info ('Initialize i2c')
    IICConfig = IIC_CONFIG()
    IICConfig.ClockSpeed = 400000
    IICConfig.Master = 1
    IICConfig.AddrBits = 7
    IICConfig.EnablePu = 1
    ret = IIC_Init(DevHandles[DevIndex],IICIndex_Sensor,byref(IICConfig));
    if ret != IIC_SUCCESS:
        logger.critical("Initialize iic faild!")
        exit()
    else:
        logger.info("Initialize iic sunccess!")

    SlaveAddr = (c_ushort * 128)()
    SlaveAddrNum = IIC_GetSlaveAddr(DevHandles[DevIndex],IICIndex_Sensor,byref(SlaveAddr))
    if SlaveAddrNum <= 0:
        logger.critical("Get iic address faild!")
        exit()
    else:
        logger.info("Get iic address sunccess!")
        SensorConnected = False
        for i in range(0,SlaveAddrNum):
            if (SlaveAddr[i] == IICAddr_Sensor):
                SensorConnected = True
                logger.info('Sensor 0x%02X Connected', SlaveAddr[i])
        if SensorConnected == False:
            logger.critical("Sensor not connect!")
            exit()

    # IIC_WriteBytes()