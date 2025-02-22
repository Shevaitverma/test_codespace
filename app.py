from flask import Flask, render_template
import subprocess
import datetime
import pytz
import os
import shlex

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Welcome to the System Monitor</h1><p>Go to <a href='/htop'>/htop</a> to view the system information.</p>"

@app.route('/htop')
def htop_page():
    full_name = "Bhasker" 
    username = os.getenv("USER")
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(ist)
    server_time_ist = now_ist.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    system_info = {}

    try:
        # CPU Usage
        cpu_usage = subprocess.check_output(['top', '-bn1', '-i', '-c'], universal_newlines=True).splitlines()[2]
        system_info['cpu_usage'] = cpu_usage

        # Memory Usage
        mem_usage = subprocess.check_output(['free', '-h'], universal_newlines=True)
        system_info['mem_usage'] = mem_usage

        # Disk Usage
        disk_usage = subprocess.check_output(['df', '-h'], universal_newlines=True)
        system_info['disk_usage'] = disk_usage

        # Processes (Top 10)
        top_processes = subprocess.check_output(['ps', 'aux', '--sort=-pcpu'], universal_newlines=True).splitlines()[:11] # Top 10 + header
        system_info['top_processes'] = "\n".join(top_processes)


    except Exception as e:
        system_info['error'] = f"An error occurred: {e}"

    return render_template('htop.html', full_name=full_name, username=username, server_time_ist=server_time_ist, system_info=system_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)