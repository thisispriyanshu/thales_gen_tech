from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
from flask_migrate import Migrate
from logging.config import dictConfig
import logging
import csv
from io import StringIO
from functools import wraps

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deepfake_detection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }, 'file': {
        'class': 'logging.FileHandler',
        'filename': 'app.log',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file']
    }
})

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    verifications = db.relationship('Verification', backref='user', lazy=True)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(32))
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)

class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(256))
    is_deepfake = db.Column(db.Boolean)
    confidence_score = db.Column(db.Float)
    report_details = db.Column(db.Text)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)

class DetectionMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verification_id = db.Column(db.Integer, db.ForeignKey('verification.id'))
    processing_time = db.Column(db.Float)
    model_version = db.Column(db.String(50))
    features_analyzed = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Export verifications
@app.route('/api/admin/export', methods=['GET'])
@jwt_required()
@admin_required
def export_verifications():
    try:
        si = StringIO()
        cw = csv.writer(si)
        verifications = Verification.query.all()
        
        # Write headers
        cw.writerow(['ID', 'User', 'Timestamp', 'Is Deepfake', 'Confidence Score'])
        
        # Write data
        for v in verifications:
            cw.writerow([v.id, v.user.username, v.timestamp, v.is_deepfake, v.confidence_score])
        
        output = si.getvalue()
        return jsonify({
            'data': output,
            'filename': f'verifications_export_{datetime.now().strftime("%Y%m%d")}.csv'
        })
    except Exception as e:
        app.logger.error(f"Export error: {str(e)}")
        return jsonify({'error': 'Export failed'}), 500

# Dashboard metrics
@app.route('/api/admin/dashboard/metrics', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_metrics():
    try:
        total_verifications = Verification.query.count()
        deepfake_count = Verification.query.filter_by(is_deepfake=True).count()
        recent_verifications = Verification.query.order_by(
            Verification.timestamp.desc()
        ).limit(10).all()
        
        return jsonify({
            'total_verifications': total_verifications,
            'deepfake_percentage': (deepfake_count / total_verifications * 100) if total_verifications > 0 else 0,
            'recent_verifications': [{
                'id': v.id,
                'timestamp': v.timestamp,
                'is_deepfake': v.is_deepfake,
                'confidence_score': v.confidence_score
            } for v in recent_verifications]
        })
    except Exception as e:
        app.logger.error(f"Dashboard metrics error: {str(e)}")
        return jsonify({'error': 'Failed to fetch metrics'}), 500

# Two-factor authentication endpoints
@app.route('/api/admin/2fa/enable', methods=['POST'])
@jwt_required()
@admin_required
def enable_2fa():
    import pyotp
    
    user = User.query.get(get_jwt_identity())
    secret = pyotp.random_base32()
    user.two_factor_secret = secret
    user.two_factor_enabled = True
    
    db.session.commit()
    
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(user.email, issuer_name="DeepfakeDetection")
    
    return jsonify({
        'secret': secret,
        'uri': provisioning_uri
    })

@app.route('/api/admin/2fa/verify', methods=['POST'])
@jwt_required()
def verify_2fa():
    import pyotp
    
    data = request.get_json()
    user = User.query.get(get_jwt_identity())
    
    if not user.two_factor_enabled:
        return jsonify({'error': '2FA not enabled'}), 400
    
    totp = pyotp.TOTP(user.two_factor_secret)
    if totp.verify(data['code']):
        # Log successful 2FA verification
        log_entry = AuditLog(
            user_id=user.id,
            action='2FA_VERIFICATION',
            details='Successful 2FA verification'
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({'message': '2FA verification successful'})
    
    return jsonify({'error': 'Invalid 2FA code'}), 401

def log_detection_result(verification_id, is_deepfake, confidence_score, processing_time):
    try:
        # Log detection metrics
        metrics = DetectionMetrics(
            verification_id=verification_id,
            processing_time=processing_time,
            model_version='1.0',  # Update this based on your AI model version
            features_analyzed={
                'confidence_score': confidence_score,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        db.session.add(metrics)
        
        # If it's a high-confidence deepfake, create a priority alert
        if is_deepfake and confidence_score > 0.85:
            app.logger.warning(f"High-confidence deepfake detected! Verification ID: {verification_id}")
            # Here you could implement notification logic (email, SMS, etc.)
            
        db.session.commit()
    except Exception as e:
        app.logger.error(f"Error logging detection result: {str(e)}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
