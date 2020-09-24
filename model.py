__title__   = 'Models Notify'
__author__  = 'ZE'


from sqlalchemy import Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base

MB = declarative_base()

class NotifyModel(MB):
    __tablename__ = 'notify'

    id = Column(String(), primary_key=True)
    ts_updt = Column(String())
    ts_recv = Column(String())
    ts_send = Column(String())
    status = Column(String())
    remittee = Column(String())
    payload = Column(JSON())

    def __repr__(self):
        '''
            Objective............: Return Object Representation
            Return...............: Return Object Representation
        '''
        return f"<NotifyModel(id='{self.id}', ts_updt='{self.ts_updt}', ts_recv='{self.ts_recv}', ts_send='{self.ts_send}', status='{self.status}', remittee='{self.remittee}', payload='{self.payload}')>"

    def to_dict(self):
        '''
            Objective............: Return Object Dict Representation
            Return...............: Return Object Dict Representation
        '''
        return {
            'id': self.id,
            'ts_updt': self.ts_updt,
            'ts_recv': self.ts_recv,
            'ts_send': self.ts_send,
            'status': self.status,
            'remittee': self.remittee,
            'payload': self.payload,
        }
