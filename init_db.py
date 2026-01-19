from app import app, db, Doctor

def init_database():
    """初始化資料庫並新增範例資料"""
    with app.app_context():
        # 建立資料表
        db.create_all()
        
        # 檢查是否已有資料
        if Doctor.query.count() > 0:
            print("資料庫已有資料，跳過初始化")
            return
        
        # 新增範例醫師資料
        sample_doctors = [
            {
                'name': '王大明',
                'phone': '0912-345-678',
                'email': 'wang@example.com',
                'specialty': '內科',
                'gender': '男',
                'status': '已簽約'
            },
            {
                'name': '李小華',
                'phone': '0923-456-789',
                'email': 'lee@example.com',
                'specialty': '外科',
                'gender': '女',
                'status': '合作中'
            },
            {
                'name': '張美玲',
                'phone': '0934-567-890',
                'email': 'chang@example.com',
                'specialty': '小兒科',
                'gender': '女',
                'status': '洽談中'
            },
            {
                'name': '陳志強',
                'phone': '0945-678-901',
                'email': 'chen@example.com',
                'specialty': '骨科',
                'gender': '男',
                'status': '已簽約'
            },
            {
                'name': '林雅婷',
                'phone': '0956-789-012',
                'email': 'lin@example.com',
                'specialty': '婦產科',
                'gender': '女',
                'status': '合作中'
            },
            {
                'name': '黃建國',
                'phone': '0967-890-123',
                'email': 'huang@example.com',
                'specialty': '眼科',
                'gender': '男',
                'status': '洽談中'
            },
            {
                'name': '吳佳穎',
                'phone': '0978-901-234',
                'email': 'wu@example.com',
                'specialty': '皮膚科',
                'gender': '女',
                'status': '已簽約'
            },
            {
                'name': '周俊傑',
                'phone': '0989-012-345',
                'email': 'chou@example.com',
                'specialty': '牙科',
                'gender': '男',
                'status': '合作中'
            }
        ]
        
        for doctor_data in sample_doctors:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
        
        db.session.commit()
        print(f"成功新增 {len(sample_doctors)} 筆範例醫師資料")

if __name__ == '__main__':
    init_database()
