# coding=utf-8
from datetime import datetime
from flask_appbuilder import Base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DateTime
from connect import session, BaseModel, engine


# All devices detected by sensor
class Eqp(BaseModel):
    __tablename__ = 'eqp'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False, default='Unknown Host')
    department = Column(String(80), nullable=False, default='Unknown Department')
    ip = Column(String(80), nullable=False)
    mac = Column(String(80))
    os = Column(String(80), nullable=False, default='Unknown OS')
    computer = Column(String(80), nullable=False, default='Unknown Computer')
    first_time = Column(DateTime)
    last_time = Column(DateTime)
    authority = Column(Integer, default=0)  # Is it a authorized equipment
    sensor_id = Column(Integer)

    def __init__(self, name, department, ip, mac, os, computer, authority, first_time, last_time, sensor_id):
        self.name = name
        self.department = department
        self.ip = ip
        self.mac = mac
        self.os = os
        self.computer = computer
        self.authority = authority
        self.first_time = datetime.now()
        self.last_time = datetime.now()
        self.sensor_id = sensor_id

    def __repr__(self):
        return '<eqp:{id}, {name}>'.format(id=self.id, name=self.name)

    @staticmethod
    def is_eqp_exist(mac, ip):
        """
        if eqp exists, return eqp.id,else return -1
        """
        eqp = session.query(Eqp).filter_by(mac=mac, ip=ip).first()
        if eqp:
            return eqp.id
        else:
            return False

    @staticmethod
    def add_eqp(name, department, ip, mac, os, computer, authority, sensor_id=None):
        """
        if eqp exists, update last_time return -1
        else, add eqp and return eqp.id
        """
        if Eqp.is_eqp_exist(mac, ip):  # eqp exists
            e = session.query(Eqp).filter_by(mac=mac, ip=ip).first()
            e.last_time = datetime.now()
            session.commit()
            return -1
        first_time = datetime.now()
        last_time = datetime.now()
        new_eqp = Eqp(name, department, ip, mac, os, computer, authority, first_time, last_time, sensor_id)
        session.add(new_eqp)
        session.commit()
        return new_eqp.id

    @staticmethod
    def get_all_eqp():
        all_eqp = session.query(Eqp).all()
        return all_eqp

    @staticmethod
    def update_auth(data):
        e = session.query(Eqp).filter_by(id=data['eqp_id']).first()
        e.authority = data['auth']
        session.commit()
        return data['eqp_id']
