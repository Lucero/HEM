from ctypes import *
import platform


BME680_SPI_INTF = 0
BME680_I2C_INTF = 1

class bme680_calib_data(Structure): 
    _fields_ = [
        ("par_h1", c_uint16),
        ("par_h2", c_uint16),
        ("par_h3", c_uint8),
        ("par_h4", c_uint8),
        ("par_h5", c_uint8),
        ("par_h6", c_uint8),
        ("par_h7", c_uint8),
        ("par_gh1", c_uint8),
        ("par_gh2", c_uint16),
        ("par_gh3", c_uint8),
        ("par_t1", c_uint16),
        ("par_t2", c_uint16),
        ("par_t3", c_uint8),
        ("par_p1", c_uint16),
        ("par_p2", c_uint16),
        ("par_p3", c_uint8),
        ("par_p4", c_uint16),
        ("par_p5", c_uint16),
        ("par_p6", c_uint8),
        ("par_p7", c_uint8),
        ("par_p8", c_uint16),
        ("par_p9", c_uint16),
        ("par_p10", c_uint8),
        ("t_fine", c_uint32),
        ("res_heat_range", c_uint8),
        ("res_heat_val", c_uint8),
        ("range_sw_err", c_uint8)
    ]

class bme680_tph_sett(Structure):
    _fields_ = [
        ("os_hum", c_uint8),
        ("os_temp", c_uint8),
        ("os_pres", c_uint8),
        ("filter", c_uint8)
    ]
    
class bme680_gas_sett(Structure):
    _fields_ = [
        ("nb_conv", c_uint8),
        ("heatr_ctrl", c_uint8),
        ("run_gas", c_uint8),
        ("heatr_temp", c_uint16),
        ("heatr_dur", c_uint16)
    ]

if(platform.system()=="Windows"):
    bme680_com_fptr_t = WINFUNCTYPE(c_uint8, c_uint8, c_uint8, c_void_p, c_uint16)# First argument is return type
    bme680_delay_fptr_t = WINFUNCTYPE(None, c_uint32)
else:
    bme680_com_fptr_t = CFUNCTYPE(c_uint8, c_uint8, c_uint8, c_void_p, c_uint16)# First argument is return type
    bme680_delay_fptr_t = CFUNCTYPE(None, c_uint32)


class bme680_dev(Structure): 
    _fields_ = [
        ("chip_id", c_uint8),
        ("dev_id", c_uint8),
        ("intf", c_uint),
        ("mem_page",c_uint8),
        ("amb_temp",c_uint8),
        ("calib",bme680_calib_data),
        ("tph_sett",bme680_tph_sett),
        ("gas_sett",bme680_gas_sett),
        ("power_mode", c_uint8),
        ("new_fields", c_uint8),
        ("info_msg", c_uint8),
        ("read", bme680_com_fptr_t),
        ("write", bme680_com_fptr_t),
        ("delay_ms", bme680_delay_fptr_t),
        ("com_rslt", c_uint8)
    ]

class bme680_field_data(Structure):
    _fields_ = [
        ("status", c_uint8),
        ("gas_index", c_uint8),
        ("meas_index", c_uint8),
        # Temperature in degree celsius x100
        ("temperature", c_uint16),
        # Pressure in Pascal
        ("pressure", c_uint32),
        # Humidity in % relative humidity x1000
        ("humidity", c_uint32),
        # Gas resistance in Ohms
        ("gas_resistance", c_uint32),
        ]


#/** Error code definitions */
BME680_OK                =  0
#/* Errors */
BME680_E_NULL_PTR		 =  -1 #255
BME680_E_COM_FAIL		 =  -2 #254
BME680_E_DEV_NOT_FOUND	 =  -3 #253
BME680_E_INVALID_LENGTH	 =  -4 #252

#/* Warnings */
BME680_W_DEFINE_PWR_MODE =  1
BME680_W_NO_NEW_DATA     =  2


#/** Power mode settings */
BME680_SLEEP_MODE	 = 0
BME680_FORCED_MODE	 = 1


#/** Over-sampling settings */
BME680_OS_NONE		= 0
BME680_OS_1X		= 1
BME680_OS_2X		= 2
BME680_OS_4X		= 3
BME680_OS_8X		= 4
BME680_OS_16X		= 5

#/** IIR filter settings */
BME680_FILTER_SIZE_0	= 0
BME680_FILTER_SIZE_1	= 1
BME680_FILTER_SIZE_3	= 2
BME680_FILTER_SIZE_7	= 3
BME680_FILTER_SIZE_15	= 4
BME680_FILTER_SIZE_31	= 5
BME680_FILTER_SIZE_63	= 6
BME680_FILTER_SIZE_127	= 7

#/** Gas measurement settings */
BME680_DISABLE_GAS_MEAS		= 0x00
BME680_ENABLE_GAS_MEAS		= 0x01


#/** Settings selector */
BME680_OST_SEL			= 1
BME680_OSP_SEL			= 2
BME680_OSH_SEL			= 4
BME680_GAS_MEAS_SEL		= 8
BME680_FILTER_SEL		= 16
BME680_HCNTRL_SEL		= 32
BME680_RUN_GAS_SEL		= 64
BME680_NBCONV_SEL		= 128
BME680_GAS_SENSOR_SEL	= (BME680_GAS_MEAS_SEL | BME680_RUN_GAS_SEL | BME680_NBCONV_SEL)


#/** Mask definitions */
BME680_GAS_MEAS_MSK	= 0x30
BME680_NBCONV_MSK	= 0X0F
BME680_FILTER_MSK	= 0X1C
BME680_OST_MSK		= 0XE0
BME680_OSP_MSK		= 0X1C
BME680_OSH_MSK		= 0X07
BME680_HCTRL_MSK	= 0x08
BME680_RUN_GAS_MSK	= 0x10
BME680_MODE_MSK		= 0x03
BME680_RHRANGE_MSK	= 0x30
BME680_RSERROR_MSK	= 0xf0
BME680_NEW_DATA_MSK	= 0x80
BME680_GAS_INDEX_MSK	= 0x0f
BME680_GAS_RANGE_MSK	= 0x0f
BME680_GASM_VALID_MSK	= 0x20
BME680_HEAT_STAB_MSK	= 0x10
BME680_MEM_PAGE_MSK	= 0x10
BME680_SPI_RD_MSK	= 0x80
BME680_SPI_WR_MSK	= 0x7f
BME680_BIT_H1_DATA_MSK	= 0x0F


