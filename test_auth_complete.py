# test_auth_complete.py
import requests
import json
import time

def complete_auth_test():
    base_url = "http://localhost:8000"
    test_phone = "+84123456789"
    
    print("🚀 Vinow认证系统完整测试")
    print("=" * 60)
    
    test_results = []
    
    # 测试1: 发送验证码
    print("\n1. 📱 发送验证码")
    try:
        send_response = requests.post(
            f"{base_url}/api/v1/auth/send-otp", 
            json={"phone": test_phone},
            timeout=10
        )
        success = send_response.status_code == 200
        test_results.append(("发送验证码", success))
        
        if success:
            send_data = send_response.json()
            code = send_data.get('data', {}).get('code')
            print(f"   ✅ 成功 - 验证码: {code}")
        else:
            print(f"   ❌ 失败 - 状态码: {send_response.status_code}")
            print(f"   错误: {send_response.text}")
            return False
    except Exception as e:
        print(f"   ❌ 异常 - {e}")
        return False
    
    # 测试2: 验证验证码
    print("\n2. 🔐 验证验证码")
    try:
        verify_response = requests.post(
            f"{base_url}/api/v1/auth/verify-otp", 
            json={"phone": test_phone, "code": code},
            timeout=10
        )
        success = verify_response.status_code == 200
        test_results.append(("验证验证码", success))
        
        if success:
            verify_data = verify_response.json()
            access_token = verify_data.get('access_token')
            refresh_token = verify_data.get('refresh_token')
            user_id = verify_data.get('user', {}).get('id')
            print(f"   ✅ 成功 - 用户ID: {user_id}")
        else:
            print(f"   ❌ 失败 - {verify_response.text}")
            return False
    except Exception as e:
        print(f"   ❌ 异常 - {e}")
        return False
    
    # 测试3: 获取用户资料
    print("\n3. 👤 获取用户资料")
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(
            f"{base_url}/api/v1/auth/profile", 
            headers=headers,
            timeout=10
        )
        success = profile_response.status_code == 200
        test_results.append(("获取用户资料", success))
        print(f"   {'✅ 成功' if success else '❌ 失败'} - 状态码: {profile_response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常 - {e}")
        test_results.append(("获取用户资料", False))
    
    # 测试4: 检查会话状态
    print("\n4. 🔍 检查会话状态")
    try:
        session_response = requests.get(
            f"{base_url}/api/v1/auth/session", 
            headers=headers,
            timeout=10
        )
        success = session_response.status_code == 200
        test_results.append(("检查会话状态", success))
        if success:
            session_data = session_response.json()
            print(f"   ✅ 成功 - 认证状态: {session_data.get('authenticated')}")
        else:
            print(f"   ❌ 失败 - 状态码: {session_response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常 - {e}")
        test_results.append(("检查会话状态", False))
    
    # 测试5: 用户重复使用
    print("\n5. 🔁 用户重复使用测试")
    try:
        time.sleep(1)  # 等待一下
        send_response2 = requests.post(
            f"{base_url}/api/v1/auth/send-otp", 
            json={"phone": test_phone},
            timeout=10
        )
        code2 = send_response2.json().get('data', {}).get('code')
        
        verify_response2 = requests.post(
            f"{base_url}/api/v1/auth/verify-otp", 
            json={"phone": test_phone, "code": code2},
            timeout=10
        )
        
        if verify_response2.status_code == 200:
            user_id2 = verify_response2.json().get('user', {}).get('id')
            same_user = user_id == user_id2
            test_results.append(("用户重复使用", same_user))
            print(f"   {'✅ 成功' if same_user else '❌ 失败'} - 用户ID: {user_id2}")
        else:
            test_results.append(("用户重复使用", False))
            print(f"   ❌ 失败 - 第二次验证失败: {verify_response2.text}")
    except Exception as e:
        print(f"   ❌ 异常 - {e}")
        test_results.append(("用户重复使用", False))
    
    # 测试6: 刷新令牌
    print("\n6. 🔄 刷新访问令牌")
    try:
        refresh_response = requests.post(
            f"{base_url}/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
            timeout=10
        )
        success = refresh_response.status_code == 200
        test_results.append(("刷新令牌", success))
        print(f"   {'✅ 成功' if success else '❌ 失败'} - 状态码: {refresh_response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常 - {e}")
        test_results.append(("刷新令牌", False))
    
    # 测试7: 调试端点
    print("\n7. 🐛 调试端点")
    try:
        codes_response = requests.get(f"{base_url}/api/v1/auth/debug/codes", timeout=10)
        sessions_response = requests.get(f"{base_url}/api/v1/auth/debug/sessions", timeout=10)
        debug_ok = codes_response.status_code == 200 and sessions_response.status_code == 200
        test_results.append(("调试端点", debug_ok))
        print(f"   {'✅ 成功' if debug_ok else '❌ 失败'} - 验证码端点: {codes_response.status_code}, 会话端点: {sessions_response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常 - {e}")
        test_results.append(("调试端点", False))
    
    # 测试8: 用户登出
    print("\n8. 🚪 用户登出")
    try:
        logout_response = requests.post(
            f"{base_url}/api/v1/auth/logout", 
            headers=headers,
            timeout=10
        )
        success = logout_response.status_code == 200
        test_results.append(("用户登出", success))
        print(f"   {'✅ 成功' if success else '❌ 失败'} - 状态码: {logout_response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常 - {e}")
        test_results.append(("用户登出", False))
    
    # 测试总结
    print("\n" + "=" * 60)
    print("📊 测试总结报告")
    print("-" * 60)
    
    passed = 0
    for test_name, success in test_results:
        status_icon = "✅" if success else "❌"
        status_text = "通过" if success else "失败"
        print(f"   {status_icon} {test_name}: {status_text}")
        if success:
            passed += 1
    
    total = len(test_results)
    success_rate = (passed / total) * 100
    
    print("-" * 60)
    print(f"🎯 通过率: {passed}/{total} ({success_rate:.1f}%)")
    
    if passed == total:
        print("🎉 所有测试通过! 认证系统工作正常。")
        return True
    elif passed >= total * 0.7:
        print("⚠️  大部分测试通过，但有部分功能需要检查。")
        return True
    else:
        print("❌ 多个测试失败，需要重点修复。")
        return False

if __name__ == "__main__":
    success = complete_auth_test()
    exit(0 if success else 1)