from flask import Flask, render_template_string
import subprocess
import os
import datetime
import pytz

app = Flask(__name__)

# Adding a root route to check if the app is working
@app.route('/')
def home():
    return "Flask app is running. Go to /htop to see system information."

@app.route('/htop')
def htop():
    # Getting username
    username = os.getenv('USER', subprocess.getoutput('whoami'))
    
    # Getting full name 
    try:
        name = subprocess.getoutput('git config --get user.name')
        if not name:
            name = "Your Full Name"  # Replace with your actual name
    except:
        name = "Your Full Name"  # Replace with your actual name
    
    # Get server time in IST
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # Get top output
    try:
        
        top_output = subprocess.getoutput('top -b -n 1')
    except:
        top_output = "Could not retrieve top output"
    
    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTOP Information</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            pre { background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
            .info { margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h1>System Information</h1>
        <div class="info">
            <p><strong>Name:</strong> {{ name }}</p>
            <p><strong>Username:</strong> {{ username }}</p>
            <p><strong>Server Time (IST):</strong> {{ server_time }}</p>
        </div>
        <h2>Top Output:</h2>
        <pre>{{ top_output }}</pre>
    </body>
    </html>
    """
    
    return render_template_string(html_template, 
                                 name=name,
                                 username=username,
                                 server_time=server_time,
                                 top_output=top_output)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)