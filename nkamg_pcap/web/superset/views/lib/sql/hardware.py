# -*- coding: utf-8 -*-
# Nankai QiuKF 1055419050@qq.com
# make table to save the inforamtion of hardware
from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, or_, desc
from sqlalchemy.types import String, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime


# All devices detected by sensor
class Hardware(BaseModel):
    __tablename__ = 'hardware'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, default='Unknown User')
    ip = Column(String(80), nullable=False, default='Unknown IP')
    mac = Column(String(80))
    os = Column(String(80), nullable=False, default='Unknown OS')
    computer = Column(String(80), nullable=False, default='Unknown Computer')
    processor = Column(String(80))
    mainboard = Column(String(80))
    memory = Column(String(80))
    disk = Column(String(80))
    xsq = Column(String(80))  # xian shi qi
    xk = Column(String(80))  # xian ka
    sk = Column(String(80))  # sheng ka
    gq = Column(String(80))  # guang qu
    wk = Column(String(80))  # wang ka
    sn = Column(String(80))  # xu lie hao

    def __init__(
            self,
            name,
            ip,
            mac,
            os,
            computer,
            processor,
            mainboard,
            memory,
            disk,
            xsq,
            xk,
            sk,
            gq,
            wk,
            sn):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.os = os
        self.computer = computer
        self.processor = processor
        self.mainboard = mainboard
        self.memory = memory
        self.disk = disk
        self.xsq = xsq
        self.xk = xk
        self.sk = sk
        self.gq = gq
        self.wk = wk
        self.sn = sn

    def __repr__(self):
        return '<hardware: %d %r>' % (self.id, self.name)

    @staticmethod
    def get_all_hardware():
        all_hardware = session.query(Hardware).all()
        return all_hardware

    @staticmethod
    def read_hardware_info(csv_name):
        import codecs
        info_csv = codecs.open(csv_name, 'r', 'gbk')
        start = info_csv.readlines()
        data = start[2:-1]  # filte export_time, column name
        for each in data:
            start = each.split(',')
            new_hardware = Hardware(
                start[0],
                start[1],
                start[2],
                start[3],
                start[4],
                start[5],
                start[6],
                start[7],
                start[8],
                start[9],
                start[10],
                start[11],
                start[12],
                start[13],
                start[17])
            session.add(new_hardware)
            session.commit()

        '''
        while start:
            start=start.split(',')
            new_hardware=Hardware(start[0],start[1],start[2],start[3],start[4],start[5],start[6],start[7],start[8],start[9],start[10],start[11],start[12],start[13],start[17])
            session.add(new_hardware)
            session.commit()
            start=info_csv.readline()
        '''
    @staticmethod
    def init():

        Base.metadata.create_all(engine)
        old = Hardware.get_all_hardware()
        if old:
            print '[i] delete old data in hardware table...'
        for item in old:
            session.delete(item)
        session.commit()

        hardware_info_csv = 'hardware_info.csv'
        Hardware.read_hardware_info(hardware_info_csv)
        print '[i] complete initing the hardware table...'

    # Change the authority of eqp
