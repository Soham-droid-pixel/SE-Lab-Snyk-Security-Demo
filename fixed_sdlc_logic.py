import json
import base64
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/load-profile')
def load_profile():
    user_data_encoded = request.cookies.get('user_profile')
    
    if user_data_encoded:
        try:
            user_data = base64.b64decode(user_data_encoded).decode('utf-8')
            
            # FIXED: Replaced unsafe 'pickle' deserialization with safe 'json' parsing.
            # json avoids arbitrary code execution that pickle is vulnerable to.
            profile = json.loads(user_data)
            
            # FIXED: Ensure 'name' is a string and use `escape()` to prevent Cross-Site Scripting (XSS).
            # We also ensure that no TypeError is thrown if 'name' is completely missing.
            name = str(profile.get('name', 'Unknown'))
            return f"Loaded profile for: {escape(name)}"
        except json.JSONDecodeError:
            return "Invalid profile data."
        except Exception:
            return "Error loading profile."
    
    return "No profile found."
