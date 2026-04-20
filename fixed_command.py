import subprocess
import re
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/network-test')
def network_test():
    target_ip = request.args.get('ip')
    
    if not target_ip:
        return "No IP provided", 400
        
    # FIXED: Added strict input validation to ensure the input is exactly an IP address.
    # This prevents any payload from being passed to the ping command entirely.
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", target_ip):
        return "Invalid IP format", 400
        
    # FIXED: Escaped the IP in the log output to prevent log injection/XSS via logs.
    print(f"Executing network test for: {escape(target_ip)}")
    
    # FIXED: Replaced os.system with subprocess.run to prevent command injection.
    # Passing arguments as a list ensures the inputs are not interpreted as shell commands.
    try:
        result = subprocess.run(["ping", "-c", "1", target_ip], capture_output=True, text=True, check=False)
        status = result.returncode
    except Exception as e:
        status = -1
    
    return f"Test completed with status: {status}"

if __name__ == "__main__":
    app.run()
