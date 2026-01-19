"""
数据库迁移脚本 - 更新表结构
运行此脚本以更新数据库表结构，删除旧的name和phone字段，添加新字段
"""
from app import app, db, Doctor
from sqlalchemy import inspect

def migrate_database():
    """迁移数据库表结构"""
    with app.app_context():
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('doctor')]
        
        print("当前数据库字段:", columns)
        
        # 检查是否需要迁移
        needs_migration = False
        
        if 'name' in columns or 'phone' in columns:
            needs_migration = True
            print("检测到旧字段，需要迁移...")
        
        if 'has_social_media' not in columns or 'social_media_link' not in columns:
            needs_migration = True
            print("检测到缺少新字段，需要迁移...")
        
        if needs_migration:
            print("\n开始迁移数据库...")
            print("警告：这将删除所有现有数据！")
            response = input("是否继续？(yes/no): ")
            
            if response.lower() == 'yes':
                # 删除旧表
                db.drop_all()
                # 创建新表
                db.create_all()
                print("数据库迁移完成！")
                print("请运行 init_db.py 重新初始化示例数据（如果需要）")
            else:
                print("迁移已取消")
        else:
            print("数据库结构已是最新，无需迁移")

if __name__ == '__main__':
    migrate_database()
