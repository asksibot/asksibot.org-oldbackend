from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import openai
import os
from dotenv import load_dotenv
# Ensure the handle_feedback_submission is appropriately referenced based on your project structure
from feedback_handler import handle_feedback_submission  

# Assuming feedback_handler.py and potentially other utility scripts remain correctly referenced

# Load environment variables from .env file
load_dotenv()

# Import the application and mail from the factory function in config.py
from config import create_app

app, mail = create_app()

# Define FlaskForm classes and routes as before

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    feedback = StringField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data['message']
    # Ensure the OPENAI_ENGINE is configured in your environment or config.py
    engine_version = app.config['OPENAI_ENGINE']  

    try:
        response = openai.Completion.create(
            engine=engine_version,  
            prompt=user_message,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
        return jsonify({'bot_response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/submit-feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        feedback_data = request.form.to_dict()
        # Ensure handle_feedback_submission is compatible with the new app structure
        handle_feedback_submission(app, feedback_data, app.config['MAIL_USERNAME'])  
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('thank_you'))

    return render_template('feedback-form.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
