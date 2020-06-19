from flask import Flask,request
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import sqlalchemy as sa
from sqlalchemy import *
from sqlalchemy.orm import scoped_session,sessionmaker
from db_connection import *

 
import pandas as pd
import jwt

#function for encoding and decoding auth tokens
def encode_credentials_jwt(user_name,pwd):
    encoded_jwt=jwt.encode({user_name: pwd}, 'secret', algorithm='HS256')
    return encoded_jwt
def decode_jwt(jwt_obtained):
    decoded_jwt=jwt.decode(jwt_obtained,'secret',algorithms=['HS256'])
    user_name=list(decoded_jwt.keys())[0]
    pwd=decoded_jwt[user_name]
    return {user_name:pwd}
# print(encoded_jwt,decoded_jwt.keys())


#2 signup api
app = Flask(__name__)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        engine = connect_sql_db('localhost:3306','root','','final')
        
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
        
        return('ok')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        engine = connect_sql_db('localhost:3306','root','','final')#hardcoded these, can be used from env file in dev environment
        #creating a session
        Session = sessionmaker(bind=engine)
        session = Session()

        
        data=request.json
        user_name=data['username']
        pwd=data['password']

        #query to match if the given username is already present in DB
        query = session.query(User).filter(User.username.in_([user_name]))
        q=query.first()
        
        #if user is present in DB, prompting him to make an account
        if q is None:
            print("no user present")
            return("User is not present. Please use Signup to create an account.")
        
        #query to match given username, pwd combo 
        query = session.query(User).filter(User.username.in_([user_name]), User.password.in_([pwd]))
        q = query.first()

        #if the combo doesn't match, prompting him with an error message.
        if q is None:
            print("no user present")
            return("Username Password combination do not match.")
        #if, verified, creating an access token,updating it in the DB to verify it in future and passing it to the client.
        else:
            print("user details verified, generating token.")
            
            authtoken=encode_credentials_jwt(user_name,pwd)
            session.query(User).filter(User.username.in_(['adminn'])).update({'authentication_token': authtoken},synchronize_session=False)
            session.commit()
            return ("user details verified. Here is your access token {}".format(authtoken))


@app.route('/auth_token',methods=['POST','GET'])
def auth_token():
    if request.method == 'POST':
        data=request.json
        engine = connect_sql_db('localhost:3306','root','','final')
        Session = sessionmaker(bind=engine)
        session = Session()
                
        auth_token_client=data['auth_token']
        print(type(auth_token_client))
        credentials_details=decode_jwt(auth_token_client)
        # query = session.query(User).filter(User.authentication_token.in_(['abcde'])).first()
        print(auth_token_client)
        user_name=list(credentials_details.keys())[0]
        pwd=credentials_details[user_name]
        print(user_name,pwd)
        # query = session.query(User).filter(User.authentication_token==auth_token_client).first()
        query = session.query(User).filter(User.username.in_([user_name]), User.password.in_([pwd]),User.authentication_token.in_([auth_token_client]))
        q = query.first()
        if query is None:
            return ('invalid auth token')
        else:
            return ('token validated.')
        

        

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


app.run(debug=True)

# {"auth_token":"b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhYmNkIjoicHdkIn0.VK8nqdPLSpiw7Iak2o7KUbzSirueRVUNCMP7Djy3I9c'"}