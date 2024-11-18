from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deepfake_detection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    verifications = db.relationship('Verification', backref='user', lazy=True)

class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(256))
    is_deepfake = db.Column(db.Boolean)
    confidence_score = db.Column(db.Float)
    report_details = db.Column(db.Text)

# User registration endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
        
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# User login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Start verification process endpoint
@app.route('/api/verify', methods=['POST'])
@jwt_required()
def start_verification():
    # Implementation for webcam verification process
    pass

# Admin endpoints
@app.route('/api/admin/verifications', methods=['GET'])
@jwt_required()
def get_verifications():
    current_user = User.query.get(get_jwt_identity())
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    verifications = Verification.query.all()
    return jsonify([{
        'id': v.id,
        'user_id': v.user_id,
        'timestamp': v.timestamp,
        'is_deepfake': v.is_deepfake,
        'confidence_score': v.confidence_score
    } for v in verifications]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
