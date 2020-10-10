# HEM
Home Environmental Monitoring



# 前言

家里有一台 笔记本改 Linux 服务器（Python代码也兼容Windows、Mac平台，验证 OK ），然后想利用这台本子监测一下家庭环境（温度、湿度、气压、空气质量），显示并记录数据。



[TOC]



# 1. 实物图

<img src=".\image\PracticalityPicture.jpg" style="zoom:25%;" />

注：右上角 ‘12.8 Hz' 为显示屏实时刷新频率，即FPS。



# 2. 模块图

![](.\image\Module.bmp)



# 3. 环境传感器

型号：BME680。他是一款四合一 MEMS 环境传感器，可测量 VOC （挥发性有机物）、温度、适度、气压，非常适用于监测空气质量。某宝价格不到50大洋。采用 IIC 接口。直接兼容 3.3V 和 5V。

<img src=".\image\BME680.png" style="zoom: 50%;" />



# 4. 显示器

0.96寸（很小巧）黄蓝双色OLED显示器，IIC接口，3.3~5V供电。分辨率128*64。某宝价格不到15大洋。

<img src=".\image\OLED.png" style="zoom: 67%;" />

# 5. 数据记录

选用 sqlite3，5分钟记录一次数据到本地数据库 ./bme680.db 内。

用 SQliteSpy 查看数据如下图：

<img src="C:\Users\Pei\Documents\HEM\image\bme680db.png" style="zoom: 80%;" />



# 6. USB2IIC

采用 Lucero LU6001 进行 USB 转 IIC。



# 7. 编程

语言选用 python，可跨平台。



# 8. 参考

5.1 BME680 驱动：https://github.com/BoschSensortec/BME680_driver

5.2 IAQ计算部分：https://github.com/PierreCASSEGRAIN/IAQ_BME680_WIPY3