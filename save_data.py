import sqlite3
from logger import *
import time

def save_data(t, h, p, r, aqi):
    # ����һ������SQLite���ݿ�����ӣ���ָ�������ݿ��ļ������ڣ����Զ�����
    conn = sqlite3.connect('bme680.db')
    # �����α����cursor����������SQL�������ݿ���в���
    c = conn.cursor()
    try:
        # �������ݱ�,SQLiteδʵ�ֱ���滻���ܣ������ݿ��ļ���Ϊ�գ���˾䱨��
        c.execute('create table bme680_db (date, time, temperature, humidity, pressure, gas_resistance, air_quality_index)')
    except:
        nothing = 0
    # ����һ����Ϣ
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
    # ������еĲ�ѯ���
    #print(c.fetchall())

    # ��������ݿ���޸�
    conn.commit()
    conn.close()