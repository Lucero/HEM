from ctypes import *
import platform
import os
import shutil

# Device info define
class DEVICE_INFO(Structure):
    _fields_ = [
        ("FirmwareName", c_char*32),   # firmware name string
        ("BuildDate", c_char*32),      # firmware build date and time string
        ("HardwareVersion", c_uint),   # hardware version
        ("FirmwareVersion",c_uint),    # firmware version
        ("SerialNumber",c_uint*3),     # Lucero serial number
        ("Functions",c_uint)           # Lucero functions
    ]

# 定义电压输出值
POWER_LEVEL_NONE    = 0 # 不输出
POWER_LEVEL_1V8     = 1 # 输出1.8V
POWER_LEVEL_2V5     = 2 # 输出2.5V
POWER_LEVEL_3V3     = 3 # 输出3.3V
POWER_LEVEL_5V0     = 4 # 输出5.0V

#根据系统自动导入对应的库文件，若没能识别到正确的系统，可以修改下面的源码
if(platform.system()=="Windows"):
    if "64bit" in platform.architecture():
        Lucero = windll.LoadLibrary( "./libs/msvc_x64/Lucero.dll" )
    else:
        Lucero = windll.LoadLibrary( "./libs/msvc_x86/Lucero.dll" )
elif(platform.system()=="Darwin"):
    Lucero = cdll.LoadLibrary( "./libs/mac_os/libLucero.dylib" )
elif(platform.system()=="Linux"):
    if 'arm' in platform.machine():
        Lucero = cdll.LoadLibrary( "./libs/Linux_ARMv7/libLucero.so" )
    else:
        if "64bit" in platform.architecture():
            Lucero = cdll.LoadLibrary( "./lib/Linux_x64/libLucero.so" )
        else:
            Lucero = cdll.LoadLibrary( "./libs/Linux_x86/libLucero.so" )
else:
    print("unsupported system")
    exit()

# Scan device
def USB_ScanDevice(pDevHandle):
    return Lucero.USB_ScanDevice(pDevHandle)

# Open device
def USB_OpenDevice(DevHandle):
    return Lucero.USB_OpenDevice(DevHandle)

# Reset device
def USB_ResetDevice(DevHandle):
    return Lucero.USB_ResetDevice(DevHandle)

# Get Lucero infomation
def DEV_GetDeviceInfo(DevHandle, pDevInfo, pFunctionStr):
    return Lucero.DEV_GetDeviceInfo(DevHandle, pDevInfo, pFunctionStr)

# Close device
def USB_CloseDevice(DevHandle):
    return Lucero.USB_CloseDevice(DevHandle)

def DEV_SetPowerLevel(DevHandle,PowerLevel):
    return Lucero.DEV_SetPowerLevel(DevHandle,PowerLevel)


