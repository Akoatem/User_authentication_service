from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index()-> str:
    return jsonify({"message": "Welcome"})
    
# Register user 
@app.route('/users', methods=['POST'])
def users() -> str:
    """_summary_
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # regsiter user if user does not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400

# Credentials validation
@app.route('/sessions', methods=['POST'])
def login() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        # create a new session
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response

@app.route('/session', methods=['POST'])
def login() ->str:
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not (Auth.valid_login(email, password)):
        abort(401)
    else:
        # create session
        session_id = Auth.create_session('email')
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        
        return response

# logout function
@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """_summary_
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')

# User profile
@app.route('/profile', methods=['GET'])
def profile() -> str:
    """_summary_
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

        
# Generate reset password token
@app.route('/reset_password', methods=['PSOT'])
def get_reset_password_token()-> str:
    email = request.form.get('email')
    try:
        reset_token = Auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort (403)
        
# Update password
@app.route('/reset_password', methods=['PUT'])
def update_password()-> str:
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        Auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password Updated"}),200
    except Exception:
        abort(403)
        
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")