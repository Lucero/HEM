from ctypes import *
from usb_device import *
from logger import *
from threading import Lock,Thread

DevHandles = (c_uint * 20)()
DevIndex = 0

dev_lock = Lock()

def device_open():
    # Scan device
    ret = USB_ScanDevice(byref(DevHandles))
    if(ret == 0):
        logger.critical("No device connected!")
        exit()
    else:
        logger.info("Have %d device connected!"%ret)

    # Open device
    ret = USB_OpenDevice(DevHandles[DevIndex])
    if(bool(ret)):
        logger.info("Open %8X device success!", DevHandles[DevIndex])
    else:
        logger.critical("Open device faild!")
        exit()

    # Get device infomation
    DevInfo = DEVICE_INFO()
    DevFunctionString = (c_char * 256)()
    ret = DEV_GetDeviceInfo(DevHandles[DevIndex],byref(DevInfo),byref(DevFunctionString))
    if(bool(ret)):
        logger.info("Lucero device infomation:" \
            "\n\tFirmware Name:\t\t%s" \
            "\n\tFirmware Version:\tv%d.%d.%d" \
            "\n\tHardware Version:\tv%d.%d.%d" \
            "\n\tBuild Date:\t\t%s" \
            "\n\tFunction String:\t%s",
                bytes(DevInfo.FirmwareName).decode('ascii'), 
                (DevInfo.FirmwareVersion>>24)&0xFF,(DevInfo.FirmwareVersion>>16)&0xFF,DevInfo.FirmwareVersion&0xFFFF,
                (DevInfo.HardwareVersion>>24)&0xFF,(DevInfo.HardwareVersion>>16)&0xFF,DevInfo.HardwareVersion&0xFFFF,
                bytes(DevInfo.BuildDate).decode('ascii'),
                bytes(DevFunctionString.value).decode('ascii'))
    else:
        logger.error("Get device infomation faild!")
        exit()
