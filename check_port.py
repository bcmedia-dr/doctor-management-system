#!/usr/bin/env python3
"""
检查端口占用情况
"""
import socket
import sys

def check_port(port):
    """检查端口是否被占用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def find_available_port(start_port=8080, max_port=8100):
    """查找可用端口"""
    for port in range(start_port, max_port + 1):
        if not check_port(port):
            return port
    return None

if __name__ == '__main__':
    print("=" * 50)
    print("🔍 检查端口占用情况")
    print("=" * 50)
    
    # 检查常用端口
    ports_to_check = [5000, 8080, 8000, 3000, 3001]
    
    for port in ports_to_check:
        if check_port(port):
            print(f"⚠️  端口 {port} 已被占用")
        else:
            print(f"✅ 端口 {port} 可用")
    
    print("\n" + "=" * 50)
    print("💡 建议:")
    print("   如果8080被占用，可以:")
    print("   1. 关闭占用8080的程序")
    print("   2. 或者修改app.py使用其他端口")
    print("=" * 50)
    
    # 查找可用端口
    available = find_available_port(8080, 8090)
    if available:
        print(f"\n✅ 建议使用端口: {available}")
