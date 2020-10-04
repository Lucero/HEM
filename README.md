# HEM
Home Environmental Monitoring



# 前言

家里有一台 nas 服务器（Linux），然后想监测一下家庭环境，显示并记录数据。



# 1. 模块图

![](.\image\Module.bmp)



# 1. 环境传感器

型号：BME680。他是一款四合一 MEMS 环境传感器，可测量 VOC （挥发性有机物）、温度、适度、气压，非常适用于监测空气质量。某宝价格不到50大洋。采用 IIC 接口。直接兼容 3.3V 和 5V。

<img src=".\image\BME680.png" style="zoom: 50%;" />



# 2. 显示器

0.96寸（很小巧）黄蓝双色OLED显示器，IIC接口，3.3~5V供电。分辨率128*64。某宝价格不到15大洋。

<img src="D:\HEM\image\OLED.png" style="zoom: 67%;" />

# 3. USB2IIC

采用 Lucero LU6001 进行 USB 转 IIC。



# 4. 编程

语言选用 python，可跨平台。



