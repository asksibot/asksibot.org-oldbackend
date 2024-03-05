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
app.config['SECRET_KEY'] = 'your_secret_key_here'

# SMTP configuration
app.config['MAIL_SERVER'] = os.environ.get('SMTP_HOST', 'smtp.titan.email')
app.config['MAIL_PORT'] = int(os.environ.get('SMTP_PORT', 465))
app.config['MAIL_USERNAME'] = os.environ.get('SMTP_USER', 'feedback@asksibot.org')
app.config['MAIL_PASSWORD'] = os.environ.get('SMTP_PASS', 'your_email_password')
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Assume you're loading the OpenAI API key from environment variables or another secure location
openai.api_key = os.environ.get('OPENAI_API_KEY', 'your_openai_api_key_here')

# Define FeedbackForm class
class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    feedback = StringField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot route
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data['message']
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Adjust as necessary
            prompt=user_message,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
        return jsonify({'bot_response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)})

# Feedback submission route
@app.route('/submit-feedback', methods=['GET', 'POST'])
def submit_feedback():
    form = FeedbackForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        feedback = form.feedback.data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = Message('Feedback Submission', sender='feedback@asksibot.org', recipients=['feedback@asksibot.org'])
        msg.body = f"Name: {name}\nEmail: {email}\nFeedback: {feedback}\nTimestamp: {timestamp}"
        mail.send(msg)
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('thank_you'))
    return render_template('feedback-form.html', form=form)

# Thank you route
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
