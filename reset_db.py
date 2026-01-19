"""
重置数据库脚本 - 删除旧数据库并创建新表结构
注意：这将删除所有现有数据！
"""
from app import app, db

def reset_database():
    """重置数据库"""
    with app.app_context():
        print("正在删除旧数据库...")
        db.drop_all()
        print("正在创建新数据库表...")
        db.create_all()
        print("数据库重置完成！")
        print("现在可以重新启动应用并添加新数据了。")

if __name__ == '__main__':
    reset_database()
