import os
from flask import Flask
from flask_mail import Mail

def create_app():
    app = Flask(__name__)

    # Retrieve SMTP configuration from environment variables
    app.config['MAIL_SERVER'] = os.environ.get('SMTP_HOST', 'smtp.titan.email')
    app.config['MAIL_PORT'] = int(os.environ.get('SMTP_PORT', 465))
    app.config['MAIL_USERNAME'] = os.environ.get('SMTP_USER', 'feedback@asksibot.org')
    app.config['MAIL_PASSWORD'] = os.environ.get('SMTP_PASS', 'your_email_password')
    app.config['MAIL_USE_SSL'] = True

    # Initialize Flask-Mail
    mail = Mail(app)

    # Define route for chatbot interactions
    @app.route('/chatbot', methods=['POST'])
    def chatbot():
        # Handle chatbot interactions securely
        # Implement the code for interacting with the chatbot here
        return 'This is the chatbot endpoint', 200

    return app, mail
