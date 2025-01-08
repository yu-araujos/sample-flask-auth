from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
  
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
  
    user = User.query.filter_by(username=username).first()
  
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        login_user(user)
        return jsonify({"message": "Login success"})
  
    return jsonify({"message": "Invalid credentials"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout success"})

@app.route('/user', methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
  
    if username and password:
        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already taken"}), 400
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user = User(username=username, password=hashed_password.decode('utf-8'), role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Sign up success"})
    
    return jsonify({"message": "Invalid data"}), 400

@app.route('/user/<int:user_id>', methods=["GET"])
@login_required
def read_user(user_id):
    user = User.query.get(user_id)
  
    if user:
        return jsonify({"username": user.username})
  
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:user_id>', methods=["PUT"])
@login_required
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)

    if user_id != current_user.id and current_user.role != 'admin':
        return jsonify({"message": "Operation not allowed"}), 403
    elif user and data.get("password"):
        hashed_password = bcrypt.hashpw(data.get("password").encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
        db.session.commit()
        return jsonify({"message": f"User {user_id} updated successfully"})
  
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:user_id>', methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if user_id != current_user.id and current_user.role != 'admin':
        return jsonify({"message": "Operation not allowed"}), 403
    elif user_id == current_user.id:
        return jsonify({"message": "Deletion not permitted for current user"}), 403
    elif user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user_id} deleted successfully"})
    else:
        return jsonify({"message": "User not found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
