from flask import Flask,request
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm import scoped_session,sessionmaker
from db_connection import *

# import 
import pandas as pd


#1a function to connect to mysql db and create a db if it is not present
# def connect_sql_db(sql_ip_port,username,pwd,db):
#     #params:
#     # sql_ip_port :(ip:port) ip and port of sqldb
#     # username : username of db user
#     # pwd : password
#     # db : database name  
#     # cnx = create_engine('mysql+pymysql://root:@localhost:3306', pool_recycle=3600)
#     connection_params = 'mysql+pymysql://'+username+':'+pwd+'@'+sql_ip_port+'/'+db
#     cnx = create_engine(connection_params,pool_recycle=3600)
#     #checking if db is present, if not creating the db
#     if not database_exists(cnx.url):
#         create_database(cnx.url)
#     return cnx


# def create_table(connection_db,tb):
#     cnx = connection_db
#     #checking if table is present in db, if not creating it
#     if not cnx.dialect.has_table(cnx, tb):  # If table don't exist, Create.
#         metadata = MetaData(cnx)
#         # Create a table with the appropriate Columns
#         Table(tb, metadata,
#             Column('SNo.', Integer), 
#             Column('username', String(255), primary_key=True, nullable=False),
#             Column('Date_created', Date), Column('password', String(255)),  Column('Auth_token', String(255)))
#         # Implement the creation
#         metadata.create_all()
#         print('HI')    
    # return cnx

# def insert_into_table(username,pwd,auth_token):
#     connection=connect_sql_db('localhost:3306','root','','finale')
#     db=scoped_session(sessionmaker(bind=connection))
#     # usernamedata=db.execute(“SELECT username FROM users WHERE {“username”=id}).fetchone
#     newToner = Toner(toner_id = 1,
#                     toner_color = 'blue',
#                     toner_hex = '#0F85FF')

#     dbsession.add(newToner)   
#     dbsession.flush()

     

    
    # cnx = create_engine(connection_params,pool_recycle=3600)
    # return cnx
    # q = cnx.execute('SHOW DATABASES')
    # available_tables = q.fetchall()
    # print(available_tables)
    # df = pd.read_sql('SELECT * FROM <table_name>', cnx)


# def database_is_empty():
#     table_names = sa.inspect(engine).get_table_names()
#     is_empty = table_names == []
#     print('Db is empty: {}'.format(is_empty))
#     return is_empty

# def table_exists(name):
#     ret = engine.dialect.has_table(engine, name)
#     print('Table "{}" exists: {}'.format(name, ret))
#     return ret
    


#2 signup api
app = Flask(__name__)
@app.route('/signup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        engine = connect_sql_db('localhost:3306','root','','finale')
        #creating a session
        Session = sessionmaker(bind=engine)
        session = Session()

        create_table(engine,Base)
        data=request.json
        user_name=data['username']
        pwd=data['password']

        

        query = session.query(User).filter(User.username.in_([user_name]))
        q=query.first()
        
        if q is None:
            print("no user present")
            user_details = User(user_name,pwd,'')
            session.add(user_details)
            session.commit()
            return("user created")

        else:
            return ("User is already present, please use login instead")
        # if query
        # # connection=connect_sql_db('localhost:3306','root','','finale')
        # db=scoped_session(sessionmaker(bind=connection))
        # # usernamedata=db.execute(“SELECT username FROM users WHERE {“username”=id}).fetchone
        # if usernamedata is None:
        #     # db.execute(“INSERT INTO users(name,username,password)
        # print('ok')
        return('ok')

# @app.route('/login', methods=['GET', 'POST'])
# cnx=connect_sql_db('localhost:3306','root','','finale')
# create_table(cnx,'tb2')

# q = cnx.table_names()
# print(type(q))
# available_tables = q.fetchall()
# print(q)
# create_db_table('db','tb','localhost:3306','root','')
# app.run()


#login api


app.run()