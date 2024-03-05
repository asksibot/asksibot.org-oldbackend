from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Mail, Message
from datetime import datetime
import openai
import os

# Initialize Flask application
app = Flask(__name__)
# Use the SECRET_KEY from the environment variable, or default to a local dev key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_secret_key_for_local_dev')

# SMTP configuration from environment variables
app.config['MAIL_SERVER'] = os.environ.get('SMTP_HOST', 'smtp.titan.email')
app.config['MAIL_PORT'] = int(os.environ.get('SMTP_PORT', 465))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Load the OpenAI API key from an environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

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
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You might want to update this to the latest model version
            prompt=user_message,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
        return jsonify({'bot_response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/submit-feedback', methods=['GET', 'POST'])
def submit_feedback():
    form = FeedbackForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        feedback = form.feedback.data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = Message('Feedback Submission', sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"Name: {name}\nEmail: {email}\nFeedback: {feedback}\nTimestamp: {timestamp}"
        mail.send(msg)
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('thank_you'))
    return render_template('feedback-form.html', form=form)

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
