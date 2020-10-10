import sqlite3
from logger import *
import time

def save_data(t, h, p, r, aqi):
    # 创建一个访问SQLite数据库的连接，当指定的数据库文件不存在，会自动创建
    conn = sqlite3.connect('bme680.db')
    # 创建游标对象cursor，用来调用SQL语句对数据库进行操作
    c = conn.cursor()
    try:
        # 创建数据表,SQLite未实现表的替换功能，若数据库文件不为空，则此句报错
        c.execute('create table bme680_db (date, time, temperature, humidity, pressure, gas_resistance, air_quality_index)')
    except:
        nothing = 0
    # 插入一条信息
    date = time.strftime("%Y-%m-%d", time.localtime())
    tim = time.strftime("%H:%M:%S", time.localtime())
    msg = "insert into bme680_db (date, time, temperature, humidity, pressure, gas_resistance, air_quality_index) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        date,
        tim,
        t,
        h,
        p,
        r,
        aqi)
    c.execute(msg)
    #c.execute('select * from bme680_db')
    # 输出所有的查询结果
    #print(c.fetchall())

    # 保存对数据库的修改
    conn.commit()
    conn.close()