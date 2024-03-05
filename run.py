from flask import render_template
from config import create_app

# Initialize Flask application
app, _ = create_app()

# Define routes for rendering HTML templates (if needed)
@app.route('/')
def home():
    return render_template('index.html')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
