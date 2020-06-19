from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref,sessionmaker
import jwt

from sqlalchemy_utils import database_exists, create_database

# engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()

class User(Base):

    __tablename__ = "registered_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(122))
    password = Column(String(122))
    authentication_token = Column(String(1222))
    def __init__(self, name, password,authentication_token):
        self.username = name
        self.password = password
        self.authentication_token=authentication_token


########################################################################
def connect_sql_db(sql_ip_port,username,pwd,db):
    #params:
    # sql_ip_port :(ip:port) ip and port of sqldb
    # username : username of db user
    # pwd : password
    # db : database name  
    # cnx = create_engine('mysql+pymysql://root:@localhost:3306', pool_recycle=3600)
    connection_params = 'mysql+pymysql://'+username+':'+pwd+'@'+sql_ip_port+'/'+db
    cnx = create_engine(connection_params,pool_recycle=3600)
    #checking if db is present, if not creating the db
    if not database_exists(cnx.url):
        create_database(cnx.url)
        print('11111databasecreated')
    print('connection to db successful')
    return cnx

def create_table(connection_db,Base_ , tb='registered_users'):
    cnx = connection_db
    #checking if table is present in db, if not creating it
    if not cnx.dialect.has_table(cnx, tb):  # If table don't exist, Create.
        Base_.metadata.create_all(cnx)
        print('Table Creation Done')    



# engine = connect_sql_db('localhost:3306','root','','finale')
# create_table(engine,Base)
# q = engine.table_names()
# print(q)


##
# Session = sessionmaker(bind=engine)
# session = Session()

# user = User("adminnn","password",'')
# session.add(user)
# session.commit()

# # query = session.query(User).filter(User.username.in_(['admin']))
# session.query(User).filter(User.username.in_(['adminn'])).update({'authentication_token': 'abcde'},synchronize_session=False)
# query = session.query(User).filter(User.authentication_token=='abcde')
# session.commit()
# q=query.first()
# print(q.authentication_token)
# if q is None:
#     print("no user present")
# else:
#     print("user present")
# # q = session.query(username).all()

# print(type(q))





#----------------------------------------------------------------------
# def __init__(self, username, password):
# """"""
# self.username = username
# self.password = password

# create tables
# Base.metadata.create_all(engine)