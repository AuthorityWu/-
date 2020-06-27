'''
此文件是用于管理record.db的创建和基础使用
record.db储存（状态->动作）关系表，记录一个状态对应动作的胜负和统计次数信息

'''

from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
import json
from data_processing import *
SQL_Address='sqlite:///../dataset/record.db'
FILE_Address='../dataset/status_count.json'
Base=declarative_base()
engine = create_engine(SQL_Address)

class NextAction(Base):
    __tablename__='next_action'
    id=Column(Integer,primary_key=True)
    init=Column(String,index=True)
    color=Column(Integer)
    move=Column(String)
    result=Column(Integer)
    count=Column(Integer)

    # 把SQLAlchemy查询对象转换成字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return str(self.to_dict())


def get_session():
    Session = scoped_session(sessionmaker(bind=engine))
    return Session()

def init():
    Base.metadata.create_all(engine)
    session=get_session()

    with open(FILE_Address,'r') as f:
        data=json.load(f)

    for record in data:
        next_action=NextAction(
            init=record['init'],
            color=record['color'],
            move=record['move'],
            result=record['result'],
            count=record['count'],
        )
        session.add(next_action)
    session.commit()

def get_record(initstring,color):
    session=get_session()
    data=[]
    for d in session.query(NextAction).filter(NextAction.init == initstring,NextAction.color==color):
        data.append(d.to_dict())
    return data

def add_record(code, move):
    init = num_split(code, step=2)
    color = 0
    ind = init.index(move[:2])
    if ind < 16:
        color = -1
    else:
        color = 1

    session=get_session()
    record = session.query(NextAction).filter(NextAction.init == code,NextAction.move==move).first()

    if record != None:
        record.count += 1
        session.flush()
        session.commit()
        return 
    else:
        new_record = NextAction(
            init=code,
            color=color,
            move=move,
            result=0,
            count=1,
        )
        session.add(new_record)
        session.commit()
        return 


# if __name__=="__main__":
#     init()
