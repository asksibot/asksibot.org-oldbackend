import os
from flask import Flask
from flask_mail import Mail

class Config:
    # Flask and security configurations
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key_for_local_dev')
    
    # Mail configurations
    MAIL_SERVER = os.environ.get('SMTP_HOST', 'smtp.titan.email')
    MAIL_PORT = int(os.environ.get('SMTP_PORT', 465))
    MAIL_USERNAME = os.environ.get('SMTP_USER', 'feedback@asksibot.org')
    MAIL_PASSWORD = os.environ.get('SMTP_PASS', 'your_email_password')
    MAIL_USE_SSL = True if os.environ.get('MAIL_USE_SSL', 'True') == 'True' else False
    
    # OpenAI configurations
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_ENGINE = os.environ.get('OPENAI_ENGINE', 'text-davinci-003')

# Below is the create_app function and other app initializations that were already part of your config.py
def create_app():
    app = Flask(__name__)
    
    # Load app configurations from the Config class
    app.config.from_object(Config)
    
    # Initialize Flask-Mail with app's configurations
    mail = Mail(app)

    # Define routes and other app configurations below as needed

    return app, mail
