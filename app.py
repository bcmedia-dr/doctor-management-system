from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kJ8mP2qL9xY3nM7tB5zX4cV6wN8bH1'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///doctors.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 資料庫模型
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    specialty = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'specialty': self.specialty,
            'gender': self.gender,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

# 權限裝飾器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({'error': '需要主管權限'}), 403
        return f(*args, **kwargs)
    return decorated_function

# 路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 簡單的登入驗證（實際應用應該使用資料庫和加密密碼）
    if username == 'admin' and password == 'admin123':
        session['logged_in'] = True
        session['is_admin'] = True
        session['username'] = username
        return jsonify({'success': True, 'is_admin': True})
    elif username == 'user' and password == 'Bcm13011579':
        session['logged_in'] = True
        session['is_admin'] = False
        session['username'] = username
        return jsonify({'success': True, 'is_admin': False})
    else:
        return jsonify({'error': '帳號或密碼錯誤'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/check_auth')
def check_auth():
    return jsonify({
        'logged_in': session.get('logged_in', False),
        'is_admin': session.get('is_admin', False),
        'username': session.get('username', '')
    })

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    if not session.get('logged_in'):
        return jsonify({'error': '請先登入'}), 401
    
    search = request.args.get('search', '')
    specialty = request.args.get('specialty', '')
    gender = request.args.get('gender', '')
    status = request.args.get('status', '')
    
    query = Doctor.query
    
    if search:
        query = query.filter(
            db.or_(
                Doctor.name.contains(search),
                Doctor.phone.contains(search),
                Doctor.email.contains(search)
            )
        )
    
    if specialty:
        query = query.filter_by(specialty=specialty)
    
    if gender:
        query = query.filter_by(gender=gender)
    
    if status:
        query = query.filter_by(status=status)
    
    doctors = query.all()
    return jsonify([doctor.to_dict() for doctor in doctors])

@app.route('/api/doctors', methods=['POST'])
def create_doctor():
    if not session.get('logged_in'):
        return jsonify({'error': '請先登入'}), 401
    
    data = request.json
    doctor = Doctor(
        name=data['name'],
        phone=data.get('phone'),
        email=data.get('email'),
        specialty=data.get('specialty'),
        gender=data.get('gender'),
        status=data.get('status', '洽談中')
    )
    
    db.session.add(doctor)
    db.session.commit()
    
    return jsonify(doctor.to_dict()), 201

@app.route('/api/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    if not session.get('logged_in'):
        return jsonify({'error': '請先登入'}), 401
    
    doctor = Doctor.query.get_or_404(id)
    data = request.json
    
    doctor.name = data.get('name', doctor.name)
    doctor.phone = data.get('phone', doctor.phone)
    doctor.email = data.get('email', doctor.email)
    doctor.specialty = data.get('specialty', doctor.specialty)
    doctor.gender = data.get('gender', doctor.gender)
    doctor.status = data.get('status', doctor.status)
    
    db.session.commit()
    
    return jsonify(doctor.to_dict())

@app.route('/api/doctors/<int:id>', methods=['DELETE'])
@admin_required
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    
    return jsonify({'message': '刪除成功'})

@app.route('/api/stats')
def get_stats():
    if not session.get('logged_in'):
        return jsonify({'error': '請先登入'}), 401
    
    total = Doctor.query.count()
    contracted = Doctor.query.filter_by(status='已簽約').count()
    cooperating = Doctor.query.filter_by(status='合作中').count()
    negotiating = Doctor.query.filter_by(status='洽談中').count()
    
    return jsonify({
        'total': total,
        'contracted': contracted,
        'cooperating': cooperating,
        'negotiating': negotiating
    })

@app.route('/api/export')
def export_excel():
    if not session.get('logged_in'):
        return jsonify({'error': '請先登入'}), 401
    
    from export import export_doctors_to_excel
    
    doctors = Doctor.query.all()
    file_path = export_doctors_to_excel(doctors)
    
    return send_file(file_path, as_attachment=True, download_name='醫師資料.xlsx')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
