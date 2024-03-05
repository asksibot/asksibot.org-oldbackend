import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Retrieve SMTP configuration from environment variables
app.config['MAIL_SERVER'] = os.environ.get('SMTP_HOST', 'smtp.titan.email')
app.config['MAIL_PORT'] = int(os.environ.get('SMTP_PORT', 465))
app.config['MAIL_USERNAME'] = os.environ.get('SMTP_USER', 'feedback@asksibot.org')
app.config['MAIL_PASSWORD'] = os.environ.get('SMTP_PASS', 'your_email_password')
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    feedback = StringField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    form = FeedbackForm()
    return render_template('index.html', form=form)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        feedback = form.feedback.data

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Send email with timestamp
        msg = Message('Feedback Submission', sender='feedback@asksibot.org', recipients=['feedback@asksibot.org'])
        msg.body = f"Name: {name}\nEmail: {email}\nFeedback: {feedback}\nTimestamp: {timestamp}"
        mail.send(msg)

        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('thank_you'))
    flash('Invalid form submission!', 'error')
    return redirect(url_for('index'))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
