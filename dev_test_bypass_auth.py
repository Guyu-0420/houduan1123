# 创建绕过认证的测试（用于开发环境）
cat > dev_test_bypass_auth.py << 'EOF'
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_without_auth():
    """测试不需要认证的功能"""
    print("🧪 开发环境测试（绕过认证）")
    
    # 测试公开端点
    endpoints = ['/', '/health', '/api/version']
    for endpoint in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"{endpoint}: {response.status_code}")
    
    # 测试发送验证码（应该能工作）
    print("\n测试发送验证码:")
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/send-otp",
        json={"phone": "+84123456789", "recaptcha_token": "dev_test"}
    )
    print(f"状态: {response.status_code}, 响应: {response.text}")

if __name__ == "__main__":
    test_without_auth()