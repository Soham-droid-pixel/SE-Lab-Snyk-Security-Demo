import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/network-test')
def network_test():
    # IMPACT: An attacker can append "; rm -rf /" to the IP address
    target_ip = request.args.get('ip')
    
    print(f"Executing network test for: {target_ip}")
    
    # Snyk will flag this as Command Injection
    status = os.system(f"ping -c 1 {target_ip}")
    
    return f"Test completed with status: {status}"

if __name__ == "__main__":
    app.run()