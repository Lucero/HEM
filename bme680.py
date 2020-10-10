from device import *
from usb2iic import *
from logger import *
from bme680_defs import *
import time
from ctypes import *
import platform
import globalvar
from save_data import *

globalvar._init()
BME680_lock = Lock()


#根据系统自动导入对应的库文件，若没能识别到正确的系统，可以修改下面的源码
if(platform.system()=="Windows"):
    if "64bit" in platform.architecture():
        BME680 = windll.LoadLibrary( "./bme680/libs/win_x64/BME680.dll" )
    else:
        BME680 = windll.LoadLibrary( "./bme680/libs/win_x86/BME680.dll" )
elif(platform.system()=="Darwin"):
    BME680 = cdll.LoadLibrary( "./bme680/libs/Macos/libBME680.dylib" )
elif(platform.system()=="Linux"):
    if 'arm' in platform.machine():
        print("unsupported system")
    else:
        if "64bit" in platform.architecture():
            BME680 = cdll.LoadLibrary( "./bme680/libs/Linux_x64/libBME680.so" )
        else:
            BME680 = cdll.LoadLibrary( "./bme680/libs/Linux_x86/libBME680.so" )
else:
    print("unsupported system")
    exit()

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



def analyze_sensor_data(data, n_meas):    
    MIN_TEMPERATURE = 0     #/* 0 degree Celsius */
    MAX_TEMPERATURE = 6000  #/* 60 degree Celsius */

    MIN_PRESSURE = 90000    #/* 900 hecto Pascals */
    MAX_PRESSURE = 110000   #/* 1100 hecto Pascals */

    MIN_HUMIDITY = 20000    #/* 20% relative humidity */
    MAX_HUMIDITY = 80000    #/* 80% relative humidity*/

    rslt = BME680_OK
    self_test_failed = 0
    i = 0
    cent_res = 0

    if ((data[0].temperature < MIN_TEMPERATURE) or (data[0].temperature > MAX_TEMPERATURE)):
        self_test_failed += 1

    if ((data[0].pressure < MIN_PRESSURE) or (data[0].pressure > MAX_PRESSURE)):
        self_test_failed += 1

    if ((data[0].humidity < MIN_HUMIDITY) or (data[0].humidity > MAX_HUMIDITY)):
        self_test_failed += 1

    for i in range(0, n_meas):
        if ((data[i].status & BME680_GASM_VALID_MSK) == 0):
            self_test_failed += 1

    if n_meas >= 6:
        cent_res = (data[3].gas_resistance + data[5].gas_resistance) / (2 * data[4].gas_resistance)

    if ((cent_res * 5) < 6):
        self_test_failed += 1

    if self_test_failed > 0:
        rslt = -6
        logger.error("bme680 data analyze invalid!!!")

    return rslt

def Sensor_Read(dev_id, reg_addr, pdata, len):
    buf = (c_uint8 * 1)()
    buf[0] = reg_addr
    databuf = (c_uint8 * len)()
    dev_lock.acquire()
    ret = IIC_WriteReadBytes(DevHandles[DevIndex],IICIndex_Sensor, dev_id, buf, 1, byref(databuf), len, 1000)
    dev_lock.release()
    memmove(c_char_p(pdata), byref(databuf), len)
    return ret

def Sensor_Write(dev_id, reg_addr, pdata, len):
    databuf = (c_uint8 * len)()
    memmove(byref(databuf), c_char_p(pdata), len)
    buf = (c_uint8 * (len + 1))()
    buf[0] = reg_addr
    for i in range(0, len):
        buf[i+1] = databuf[i]
    dev_lock.acquire()
    ret = IIC_WriteBytes(DevHandles[DevIndex],IICIndex_Sensor, dev_id, buf, (len+1), 1000)
    dev_lock.release()
    return ret

def Sensor_Delay_ms(period):
    period /= 1000
    time.sleep(period)
    return

def bme680_thread():
    dev = bme680_dev()
    dev.dev_id = IICAddr_Sensor
    dev.amb_temp = 25
    dev.read = bme680_com_fptr_t(Sensor_Read)
    dev.write = bme680_com_fptr_t(Sensor_Write)
    dev.intf = BME680_I2C_INTF
    dev.delay_ms = bme680_delay_fptr_t(Sensor_Delay_ms)

    rslt = BME680.bme680_init(byref(dev))
    rslt &= 0xFF
    if rslt != BME680_OK:
        logger.critical("BME680 init faild!\nError Code: 0x%X", rslt)
        exit()
    logger.info("BME680 init succeed :)")

    logger.info("BME680 config")
    #/* Set the temperature, pressure and humidity & filter settings */
    dev.tph_sett.os_hum = BME680_OS_2X
    dev.tph_sett.os_pres = BME680_OS_4X
    dev.tph_sett.os_temp = BME680_OS_8X
    dev.tph_sett.filter = BME680_FILTER_SIZE_3
    
    #/* Select the power mode */
    #/* Must be set before writing the sensor configuration */
    dev.power_mode = BME680_FORCED_MODE
    
    #/* Set the remaining gas sensor settings and link the heating profile */
    dev.gas_sett.run_gas = BME680_ENABLE_GAS_MEAS
    dev.gas_sett.heatr_temp = 320
    dev.gas_sett.heatr_dur = 150

    settings_sel = BME680_OST_SEL | BME680_OSP_SEL | BME680_OSH_SEL | BME680_GAS_SENSOR_SEL | BME680_FILTER_SEL

    #/* Set the desired sensor configuration */=
    rslt = BME680.bme680_set_sensor_settings(settings_sel, byref(dev))
    if rslt != BME680_OK:
        logger.error("Set the desired sensor configuration failed!!!")

    #/* Set the power mode */
    rslt = BME680.bme680_set_sensor_mode(byref(dev))
    if rslt != BME680_OK:
        logger.error("Set the power mode failed!!!")
        
    #/* Get the total measurement duration so as to sleep or wait till the measurement is complete */
    profile_dur = c_uint16()
    BME680.bme680_get_profile_dur(byref(profile_dur), byref(dev))
    
    # Collect gas resistance burn-in values, then use the average
    # of the last 50 values to set the upper limit for calculating
    # gas_baseline.
    burn_in_time = 300
    burn_in_data = []
    
    # Set the humidity baseline to 40%, an optimal indoor humidity.
    hum_baseline = 40.0

    # This sets the balance between humidity and gas reading in the
    # calculation of air_quality_score (25:75, humidity:gas)
    hum_weighting = 0.25

    elapsed = 0
    air_quality_index = 0
    savedata_time = 0
    while True:
        start = time.perf_counter()
            
        Sensor_Delay_ms(profile_dur.value * 2)

        data = (bme680_field_data)()
        rslt = BME680.bme680_get_sensor_data(byref(data), byref(dev))
        if rslt == BME680_OK and ((data.status & BME680_HEAT_STAB_MSK) > 0):
            if burn_in_time > 0:
                gas = data.gas_resistance
                burn_in_data.append(gas)
                if burn_in_time <=  elapsed:
                    gas_baseline = sum(burn_in_data[-50:]) / 50.0
                    logger.info('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(gas_baseline, hum_baseline))
                burn_in_time -= elapsed
                logger.info('Burn in remain {:.0f}s'.format(burn_in_time))
                
            temp = data.temperature / 100.0 #摄氏度
            hum = data.humidity / 1000.0 #百分比
            press = pressure = data.pressure / 1000.0 #帕斯卡
            gas = gas_resistance = data.gas_resistance #欧姆

            if burn_in_time <= 0:
                hum_offset = hum - hum_baseline
                gas_offset = gas_baseline - gas

                # Calculate hum_score as the distance from the hum_baseline.
                if hum_offset > 0:
                    hum_score = (100 - hum_baseline - hum_offset)
                    hum_score /= (100 - hum_baseline)
                    hum_score *= (hum_weighting * 100)

                else:
                    hum_score = (hum_baseline + hum_offset)
                    hum_score /= hum_baseline
                    hum_score *= (hum_weighting * 100)

                # Calculate gas_score as the distance from the gas_baseline.
                if gas_offset > 0:
                    gas_score = (gas / gas_baseline)
                    gas_score *= (100 - (hum_weighting * 100))

                else:
                    gas_score = 100 - (hum_weighting * 100)

                # Calculate air_quality_score.
                air_quality_score = hum_score + gas_score
                # Calculate air_quality_index. From 0 (Good) to 500 (Bad).
                
                air_quality_index =  500 * (1- (air_quality_score/100))

            seaLevel = 1013.25 # hPa
            atmospheric = pressure * 10.0
            altitude = 44330.0 * (1.0 - pow(atmospheric / seaLevel, 0.1903)) #米

            BME680_lock.acquire()
            globalvar.set_value('BME680_Temperature', temp)
            globalvar.set_value('BME680_Humidity', hum)
            globalvar.set_value('BME680_Pressure', press)
            globalvar.set_value('BME680_AQI', air_quality_index)
            BME680_lock.release()

            if start > savedata_time:
                savedata_time = time.perf_counter()
                savedata_time += 5*60
                save_data(temp, hum, press, gas_resistance, air_quality_index)

            #logger.info("\n\t温度：\t{:.2f} ℃ \
            #\n\t湿度：\t{:.2f} %RH \
            #\n\tAQI：\t{:.2f} \
            #\n\t压强：\t{:.3f} kPa \
            #\n\tRES：\t{:d} Ohms \
            #\n\t海拔： \t{:.2f} m".format(
            #    data.temperature / 100,
            #    data.humidity / 1000,
            #    air_quality_index,
            #    data.pressure / 1000,
            #    data.gas_resistance,
            #    altitude
            #))
        elif (data.status & BME680_HEAT_STAB_MSK) == 0:
            logger.warn('Sensor data still not stable!')
        else:
            logger.error("Get the sensor data failed!!!")

        elapsed = (time.perf_counter() - start)

        #/* Trigger the next measurement if you would like to read data out continuously */
        if (dev.power_mode == BME680_FORCED_MODE):
            rslt = BME680.bme680_set_sensor_mode(byref(dev))


def bme680_thread_start():
    t1=Thread(target=bme680_thread)
    t1.setDaemon(True)
    t1.start()
