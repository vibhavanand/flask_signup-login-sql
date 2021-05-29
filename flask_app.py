from flask import Flask,request,jsonify
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
        engine = connect_sql_db('localhost:3306','root','','done')
        
        #creating a session
        Session = sessionmaker(bind=engine)
        session = Session()

        create_table(engine,Base)
        data=request.json
        try:
            user_name=data['username']
            pwd=data['password']
        except:
            return jsonify({"success":"False","msg":"Invalid Req Body"})

        
        #checking if the username entered exists in the database
        query = session.query(User).filter(User.username.in_([user_name]))
        q=query.first()
        #if user doesn't exist, creating a new user
        if q is None:
            print("no user present")
            user_details = User(user_name,pwd,'')
            session.add(user_details)
            session.commit()
            return jsonify({"success":"True","msg":"User Created"})
        #if user exists
        else:
            return jsonify({"success":"False","msg":"User is already present, please use login instead"})
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        engine = connect_sql_db('localhost:3306','root','password','done')#hardcoded these, can be used from env file in dev environment later
        #creating a session
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            data=request.json
            user_name=data['username']
            pwd=data['password']
        except:
            return jsonify({"success":"False","msg":"Invalid Req Parameters"})

        #query to match if the given username is present in DB
        query = session.query(User).filter(User.username.in_([user_name]))
        q=query.first()
        
        #if user is not present in DB, prompting him to make an account
        if q is None:
            print("no user present")
            return jsonify({"success":"False","msg":"User is not present. Please use Signup to create an account."})
        
        #query to match given username, pwd combo 
        query = session.query(User).filter(User.username.in_([user_name]), User.password.in_([pwd]))
        q = query.first()

        #if the combo doesn't match, prompting him with an error message.
        if q is None:
            return jsonify({"success":"False","msg":"Username, Password combination does not match."})
        #if verified, creating an access token,updating it in the DB to verify it in future and passing it to the client.
        else:
            print("user details verified, generating token.")
            
            authtoken=encode_credentials_jwt(user_name,pwd).decode("utf-8")#first encoding the username pwd, then converting the byte object to string
            session.query(User).filter(User.username.in_(['adminn'])).update({'authentication_token': authtoken},synchronize_session=False)
            session.commit()
            return jsonify({"success":"True","msg":"user verified","Access_token":authtoken})
    if request.method == 'GET':
        return jsonify({"message": "be a dear and send correct parameters"})


@app.route('/auth_token',methods=['POST','GET'])
def auth_token():
    if request.method == 'POST':
        data=request.json
        engine = connect_sql_db('localhost:3306','root','','done')
        Session = sessionmaker(bind=engine)
        session = Session()

        #extracting auth token and converting it into a byte string for using the decode_jwt function.        
        try:
            access_token_client=data['Access_token']
        except:
            return jsonify({"success":"False","msg":"Invalid Req Parameters"})
            
        # access_token_client=access_token_client

        # string with encoding 'utf-8'
        access_token_client = bytes(access_token_client, 'utf-8')

        #checking if the token is valid
        try:
            credentials_details=decode_jwt(access_token_client)
        except Exception as  e:
            return jsonify({"success":"False","msg":"Invalid Token"})
        
        user_name=list(credentials_details.keys())[0]
        pwd=credentials_details[user_name]
        
        #checking if the credentials obtained from decoding token match in our DB.
        query = session.query(User).filter(User.username.in_([user_name]), User.password.in_([pwd]),User.authentication_token.in_([access_token_client]))
        q = query.first()
        if query is None:
            return jsonify({"success":"False","msg":"token data and credentials don't match"})
            
        else:
            return jsonify({"success":"True","msg":'token and crerdentials validated.'})
        

        


app.run(debug=True)

