#importing the packages
import os 
import bcrypt
from flask import Flask 
from flask_jwt_extended import JWTManager 
from flask_cors import CORS 
from application.config import LocalDevelopmentConfig 
from application.database import db
from application.cache import cache
from application.workers import celery_app 
from application.tasks import *

app= None

def create_app(): #function to initialize the flask app and celery

    app = Flask(__name__)
    JWTManager(app)

    if os.getenv('ENV', 'development')=='production':
        raise Exception('Currently no production config is setup')
    else:
        print('Staring Local Development')
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)

    cache.init_app(app)

    #initializing the celery configuration
    celery_app.conf.update(
        broker_url = app.config['CELERY_BROKER_URL'],
        result_backend = app.config['CELERY_RESULT_BACKENED'],
        timezone = app.config['CELERY_TIMEZONE']
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery_app.Task = ContextTask
    app.app_context().push()
    
    return app,celery_app

app,celery_app= create_app()
CORS(app, origins="http://localhost:5173") #mentioning the origin so that cors doesnot block the connection in backened


#Import all the controllers so they are loaded 
from application.user_controller import * 

if __name__ == '__main__':
    #Run the Flask app
    #creation of admin
    user = User.query.filter_by(username='admin').first()
    if user is None:
        user = User()
        user.username = 'admin'
        user.password = bcrypt.generate_password_hash('adminpassword').decode('utf-8') #storing the password in hash format
        user.is_admin = 1 #used for differentiating between admin and user
        user.email = 'ticketShow@admin.com'

        db.session.add(user)
        db.session.commit()
    app.run(debug = True, host = '0.0.0.0', port =8081)