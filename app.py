from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from functools import wraps
from sqlalchemy import inspect
from werkzeug.utils import secure_filename

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
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    specialty = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    status = db.Column(db.String(20))
    contact_person = db.Column(db.String(50))
    has_social_media = db.Column(db.String(10))  # 經營社群：是、否
    social_media_link = db.Column(db.String(500))  # 醫師社群連結
    current_brand = db.Column(db.String(200))  # 目前合作品牌
    price_range = db.Column(db.String(100))  # 報價區間
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'specialty': self.specialty,
            'gender': self.gender,
            'status': self.status,
            'contact_person': self.contact_person,
            'has_social_media': self.has_social_media,
            'social_media_link': self.social_media_link,
            'current_brand': self.current_brand,
            'price_range': self.price_range,
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
    if username == 'admin' and password == 'Bcm13011579!@':
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
    has_social_media = request.args.get('has_social_media', '')
    
    query = Doctor.query
    
    if search:
        query = query.filter(
            Doctor.email.contains(search)  # email字段存储醫師名称
        )
    
    if specialty:
        query = query.filter_by(specialty=specialty)
    
    if gender:
        query = query.filter_by(gender=gender)
    
    if status:
        query = query.filter_by(status=status)
    
    if has_social_media:
        query = query.filter_by(has_social_media=has_social_media)
    
    doctors = query.all()
    return jsonify([doctor.to_dict() for doctor in doctors])

@app.route('/api/doctors', methods=['POST'])
def create_doctor():
    if not session.get('logged_in'):
        return jsonify({'error': '請先登入'}), 401
    
    try:
        data = request.json
        doctor = Doctor(
            name=data.get('name'),
            email=data.get('email'),
            specialty=data.get('specialty'),
            gender=data.get('gender'),
            status=data.get('status', '未聯繫'),  # 默认状态改为未聯繫
            contact_person=data.get('contact_person'),
            has_social_media=data.get('has_social_media'),
            social_media_link=data.get('social_media_link'),
            current_brand=data.get('current_brand'),
            price_range=data.get('price_range')
        )
        
        db.session.add(doctor)
        db.session.commit()
        
        return jsonify(doctor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'儲存失敗：{str(e)}'}), 500

@app.route('/api/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    if not session.get('logged_in'):
        return jsonify({'error': '請先登入'}), 401
    
    try:
        doctor = Doctor.query.get_or_404(id)
        data = request.json
        
        doctor.name = data.get('name', doctor.name)
        doctor.email = data.get('email', doctor.email)
        doctor.specialty = data.get('specialty', doctor.specialty)
        doctor.gender = data.get('gender', doctor.gender)
        doctor.status = data.get('status', doctor.status)
        doctor.contact_person = data.get('contact_person', doctor.contact_person)
        doctor.has_social_media = data.get('has_social_media', doctor.has_social_media)
        doctor.social_media_link = data.get('social_media_link', doctor.social_media_link)
        doctor.current_brand = data.get('current_brand', doctor.current_brand)
        doctor.price_range = data.get('price_range', doctor.price_range)
        
        db.session.commit()
        
        return jsonify(doctor.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失敗：{str(e)}'}), 500

@app.route('/api/doctors/<int:id>', methods=['DELETE'])
@admin_required
def delete_doctor(id):
    try:
        doctor = Doctor.query.get_or_404(id)
        db.session.delete(doctor)
        db.session.commit()
        
        return jsonify({'message': '刪除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'刪除失敗：{str(e)}'}), 500

@app.route('/api/stats')
def get_stats():
    if not session.get('logged_in'):
        return jsonify({'error': '請先登入'}), 401
    
    total = Doctor.query.count()
    contracted = Doctor.query.filter_by(status='已簽約').count()
    cooperated = Doctor.query.filter_by(status='合作過').count()
    
    return jsonify({
        'total': total,
        'contracted': contracted,
        'cooperated': cooperated
    })

@app.route('/api/export')
@admin_required
def export_excel():
    from export import export_doctors_to_excel
    
    doctors = Doctor.query.all()
    file_path = export_doctors_to_excel(doctors)
    
    return send_file(file_path, as_attachment=True, download_name='醫師資料.xlsx')

@app.route('/api/import', methods=['POST'])
@admin_required
def import_excel():
    if 'file' not in request.files:
        return jsonify({'error': '沒有選擇檔案'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '沒有選擇檔案'}), 400
    
    # 檢查檔案格式（只支援 openpyxl 支援的格式）
    allowed_extensions = ('.xlsx', '.xlsm', '.xltx', '.xltm')
    if not file.filename.lower().endswith(allowed_extensions):
        return jsonify({
            'error': '檔案格式錯誤',
            'message': f'請上傳 Excel 檔案（支援格式：.xlsx、.xlsm、.xltx、.xltm）。如果您的檔案是 .xls 格式，請先用 Excel 轉換為 .xlsx 格式。'
        }), 400
    
    try:
        # 儲存上傳的檔案
        upload_folder = '/tmp'
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, f'import_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{filename}')
        file.save(file_path)
        
        # 匯入資料
        from import_data import import_doctors_from_excel
        result = import_doctors_from_excel(file_path, db, Doctor)
        
        # 刪除臨時檔案
        try:
            os.remove(file_path)
        except:
            pass
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'成功匯入 {result["success_count"]} 筆資料',
                'success_count': result['success_count'],
                'errors': result['errors']
            })
        else:
            return jsonify({
                'success': False,
                'error': '匯入失敗',
                'errors': result['errors']
            }), 500
            
    except Exception as e:
        return jsonify({'error': f'匯入失敗：{str(e)}'}), 500

def init_database():
    """初始化数据库，检查并更新表结构"""
    with app.app_context():
        try:
            # 检查表是否存在
            inspector = inspect(db.engine)
            if 'doctor' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('doctor')]
                
                # 检查是否需要迁移（旧字段存在或新字段不存在）
                needs_migration = (
                    'phone' in columns or 
                    'name' not in columns or
                    'has_social_media' not in columns or 
                    'social_media_link' not in columns or
                    'current_brand' not in columns or
                    'price_range' not in columns
                )
                
                if needs_migration:
                    print("检测到数据库结构需要更新，正在迁移...")
                    # 删除旧表
                    db.drop_all()
                    # 创建新表
                    db.create_all()
                    print("数据库迁移完成！")
                else:
                    # 确保表存在
                    db.create_all()
            else:
                # 表不存在，直接创建
                db.create_all()
                print("数据库表已创建")
        except Exception as e:
            print(f"数据库初始化错误: {e}")
            # 如果出错，尝试直接创建
            db.create_all()

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()  # ✅ 只建立表格結構,不會清空數據
            print("數據庫表已創建")
        except Exception as e:
            print(f"數據庫初始化錯誤: {e}")
            db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
