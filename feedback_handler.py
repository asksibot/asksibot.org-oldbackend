from flask_mail import Message
from datetime import datetime

def handle_feedback_submission(app, feedback_data, recipient):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_message = "\n".join([f"{key}: {value}" for key, value in feedback_data.items()]) + f"\nTimestamp: {timestamp}"
    
    msg = Message('Asksibot Feedback Submission', sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = feedback_message
    app.extensions['mail'].send(msg)
