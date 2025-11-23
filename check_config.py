# check_config.py - 配置检查脚本
import os
from dotenv import load_dotenv

print("🔍 开始配置检查")
print("=" * 50)

# 1. 检查 .env 文件是否存在
print("1. 检查 .env 文件...")
if os.path.exists('.env'):
    print("   ✅ .env 文件存在")
    
    # 加载环境变量
    load_dotenv('.env')
    
    # 2. 检查关键环境变量
    print("\n2. 检查关键环境变量:")
    
    env_vars = {
        'SUPABASE_URL': {
            'value': os.getenv('SUPABASE_URL'),
            'valid': lambda v: v and v != 'https://your-project-ref.supabase.co' and v.startswith('https://')
        },
        'SUPABASE_SERVICE_KEY': {
            'value': os.getenv('SUPABASE_SERVICE_KEY'), 
            'valid': lambda v: v and v != 'your-service-role-key-here' and len(v) > 20
        },
        'SECRET_KEY': {
            'value': os.getenv('SECRET_KEY'),
            'valid': lambda v: v and v != 'change-this-to-a-real-secret-key' and len(v) > 20
        },
        'ENVIRONMENT': {
            'value': os.getenv('ENVIRONMENT'),
            'valid': lambda v: v in ['development', 'production']
        }
    }
    
    all_valid = True
    for var_name, config in env_vars.items():
        value = config['value']
        is_valid = config['valid'](value)
        
        if not value:
            print(f"   ❌ {var_name}: 未设置")
            all_valid = False
        elif not is_valid:
            print(f"   ❌ {var_name}: 使用示例值或格式错误")
            print(f"       当前值: {value}")
            all_valid = False
        else:
            # 隐藏敏感信息的部分内容
            if var_name in ['SUPABASE_SERVICE_KEY', 'SECRET_KEY']:
                display_value = value[:10] + '...' + value[-10:] if len(value) > 20 else '***'
            else:
                display_value = value
            print(f"   ✅ {var_name}: {display_value}")
    
    # 3. 测试配置导入
    print("\n3. 测试配置导入...")
    try:
        from app.common.config import settings
        print("   ✅ 配置导入成功")
        print(f"      环境: {settings.environment}")
        print(f"      Debug模式: {settings.debug}")
        print(f"      API端口: {settings.api_port}")
        
        # 测试Supabase连接
        print("\n4. 测试Supabase连接...")
        try:
            from app.database.supabase_client import supabase
            if supabase:
                print("   ✅ Supabase客户端创建成功")
                # 尝试简单查询
                result = supabase.table('user_profiles').select('count', count='exact').limit(1).execute()
                print("   ✅ Supabase连接测试成功")
            else:
                print("   ❌ Supabase客户端创建失败")
                all_valid = False
        except Exception as e:
            print(f"   ❌ Supabase连接失败: {e}")
            all_valid = False
            
    except Exception as e:
        print(f"   ❌ 配置导入失败: {e}")
        all_valid = False
        
else:
    print("   ❌ .env 文件不存在")
    all_valid = False

print("\n" + "=" * 50)
if all_valid:
    print("🎉 所有配置检查通过！")
    print("现在可以运行: python main.py")
else:
    print("❌ 配置检查失败")
    print("\n📋 需要修复的问题:")
    if not os.path.exists('.env'):
        print("   - 创建 .env 文件")
    else:
        env_vars_to_check = ['SUPABASE_URL', 'SUPABASE_SERVICE_KEY', 'SECRET_KEY']
        for var in env_vars_to_check:
            value = os.getenv(var)
            if not value or 'your-' in str(value) or 'change-this' in str(value):
                print(f"   - 设置真实的 {var}")