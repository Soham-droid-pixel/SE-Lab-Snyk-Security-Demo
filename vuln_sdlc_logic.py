import pickle
import base64
from flask import Flask, request

app = Flask(__name__)

@app.route('/load-profile')
def load_profile():
    # SDLC ISSUE: Trusting serialized data from a client-side cookie
    # An attacker can craft a 'pickle' object that executes code when loaded
    user_data_encoded = request.cookies.get('user_profile')
    
    if user_data_encoded:
        user_data = base64.b64decode(user_data_encoded)
        
        # Snyk Code will flag 'pickle.loads' as a Critical Insecure Deserialization risk
        profile = pickle.loads(user_data)
        
        return f"Loaded profile for: {profile.get('name')}"
    
    return "No profile found."