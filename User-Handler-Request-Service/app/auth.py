from flask import Flask,request, render_template,redirect,session
from flask_sqlalchemy import SQLAlchemy #Database inbuilt module
import bcrypt
from flask import flash #allows to display messages on the screen
#from app import create_nginx_pod
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask import Blueprint


auth_blueprint = Blueprint('auth', __name__)

#database instance
#Creates a SQLAlchemy object with the Flask app as a parameter
db = SQLAlchemy()


login_manager = LoginManager()


#table creation and class User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  #id is primary key
    name = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), unique=True) #email is unique
    password = db.Column(db.String(100))

    #Initilise the entry 
    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        #Encrypted password using this module bcrypt and export the the password in db with encryption
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#Check conditions for login
    def check_password(self,password):
        #self.password is user password which mention on table when user enter
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

#@app.route('/register', methods=['GET','POST']) #GET as well as POST method use in /register endpoints
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register(): # register function
    if request.method == 'POST':
        #here we write out logic code for register
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # display data input in logs
        print(f'name: {name}')
        print(f'email: {email}')
        print(f'password1: {password}')

        #When new user enter their name email and password take the value from User class
        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)  #staging 
        #write in db
        db.session.commit()
        flash('User created')
        print('User created successfully')

        

        return redirect('login')
    

    return render_template('register.html')


#GET as well as POST method use in /login endpoints
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login(): #login function
    if request.method == 'POST':  #if request is post else render the template
        #here we write out logic code for login
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()  #get first user from db check email is exist on db or not

        #if user and user.check_password(password):    #password matching  if yes
         #   session['name'] = user.name                 #session create and redirect to /dashboard
         #   session['email'] = user.email
        #    session['password'] = user.password
          #  return redirect('/create')
        #else:
         #   return render_template('login.html',error='Invalid user')



        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            return redirect('/create')
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')





