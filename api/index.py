"""
Vercel Serverless Function
"""
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading index: {str(e)}", 500

@app.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        return f"Error loading about: {str(e)}", 500

@app.route('/documentation')
def documentation():
    try:
        return render_template('documentation.html')
    except Exception as e:
        return f"Error loading documentation: {str(e)}", 500

def handler(request):
    """Vercel serverless handler"""
    return app(request.environ, lambda status, headers: None)
