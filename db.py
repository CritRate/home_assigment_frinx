import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import json
import sys

Base = declarative_base()

class Interface(Base):
    __tablename__ = 'interfaces'

    id = Column(Integer, primary_key=True)
    connection = Column(Integer)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    config = Column(JSON)
    type = Column(String(50))
    infra_type = Column(String(50))
    port_channel_id = Column(Integer)
    max_frame_size = Column(Integer)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return (
            f'id:{self.id}\n'
            f'name:{self.name}\n'
            f'desciption:{self.description}\n'
            f'config:{self.config}\n'
            f'port channel:{self.port_channel_id}\n'
            f'max frame size:{self.max_frame_size}\n'
        )


def get_interface(session, name):
    return session.query(Interface).filter(Interface.name==name).one()

def create_session(user, password, ip, port, db_name):
    try:
        engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{ip}:{port}/{db_name}')
        # create Table if it does not exist
        Interface.__table__.create(bind=engine, checkfirst=True)
        Session = sessionmaker()
        Session.configure(bind=engine)
        return Session()
    except sqlalchemy.exc.SQLAlchemyError as e:
        sys.exit(e)

# helper functions for the assignment
def add_interface(session, name, description=None, config=None,port_channel_id=None,max_frame_size=None):
    if not name:
        raise ValueError('Name is required')
    session.add(
        Interface(
            name=name,
            description=description,
            config=json.dumps(config),
            port_channel_id=port_channel_id,
            max_frame_size=max_frame_size
    ))

def delete_interface_table_data(session):
    print('Deleting old table data.')
    session.query(Interface).delete()

