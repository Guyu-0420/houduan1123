#!/usr/bin/env python3
"""
商家系统模块目录结构一键生成脚本
运行: python scripts/create_merchant_structure.py
"""

import os
import sys

def create_file(path, content=""):
    """创建文件"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 创建文件: {path}")

def create_merchant_structure():
    """创建商家系统完整目录结构"""
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 定义商家系统目录结构
    structure = [
        # 主应用目录
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "app/dependencies.py",
        
        # Core 核心模块
        "app/core/__init__.py",
        "app/core/security.py",
        "app/core/exceptions.py",
        "app/core/middleware.py",
        "app/core/constants.py",
        
        # Models 商家数据模型
        "app/models/__init__.py",
        "app/models/base.py",
        "app/models/merchant_models.py",
        "app/models/product_models.py",
        "app/models/order_models.py",
        "app/models/marketing_models.py",
        "app/models/analytics_models.py",
        "app/models/reservation_models.py",
        
        # Schemas 商家数据验证
        "app/schemas/__init__.py",
        "app/schemas/base.py",
        "app/schemas/merchant_schemas.py",
        "app/schemas/product_schemas.py",
        "app/schemas/order_schemas.py",
        "app/schemas/marketing_schemas.py",
        "app/schemas/analytics_schemas.py",
        "app/schemas/reservation_schemas.py",
        
        # Routers 商家路由
        "app/routers/__init__.py",
        "app/routers/merchant_router.py",
        "app/routers/product_router.py",
        "app/routers/order_router.py",
        "app/routers/marketing_router.py",
        "app/routers/analytics_router.py",
        "app/routers/reservation_router.py",
        "app/routers/upload_router.py",
        
        # Services 商家业务服务
        "app/services/__init__.py",
        "app/services/merchant_service.py",
        "app/services/product_service.py",
        "app/services/order_service.py",
        "app/services/marketing_service.py",
        "app/services/analytics_service.py",
        "app/services/reservation_service.py",
        "app/services/notification_service.py",
        "app/services/file_service.py",
        "app/services/google_maps_service.py",
        "app/services/qrcode_service.py",
        
        # Utils 工具类
        "app/utils/__init__.py",
        "app/utils/auth.py",
        "app/utils/validators.py",
        "app/utils/formatters.py",
        "app/utils/date_utils.py",
        "app/utils/image_utils.py",
        "app/utils/excel_utils.py",
        "app/utils/cache.py",
        "app/utils/response.py",
        
        # Tasks 商家后台任务
        "app/tasks/__init__.py",
        "app/tasks/analytics_tasks.py",
        "app/tasks/notification_tasks.py",
        "app/tasks/cleanup_tasks.py",
        
        # Tests 商家测试文件
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/test_merchant.py",
        "tests/test_product.py",
        "tests/test_order.py",
        "tests/test_marketing.py",
        "tests/test_analytics.py",
        "tests/test_reservation.py",
        
        # Scripts 商家脚本
        "scripts/__init__.py",
        "scripts/create_merchant_structure.py",
        "scripts/init_database.py",
        "scripts/seed_merchant_data.py",
        
        # 配置文件
        "requirements.txt",
        ".env",
        ".gitignore",
        "docker-compose.yml",
        "Dockerfile",
        "README.md"
    ]
    
    print("🚀 开始创建商家系统模块目录结构...")
    
    for file_path in structure:
        full_path = os.path.join(base_dir, file_path)
        
        # 为不同文件类型提供基础内容
        content = ""
        if file_path.endswith("__init__.py"):
            content = '"""商家系统模块"""\n'
        elif file_path.endswith(".py") and not file_path.endswith("__init__.py"):
            filename = os.path.basename(file_path).replace('.py', '')
            content = f'"""商家系统 - {filename}"""\n\n# TODO: 实现商家系统相关功能\n'
        
        create_file(full_path, content)
    
    # 创建静态文件目录
    static_dirs = [
        "static/qrcodes",
        "static/uploads"
    ]
    
    for dir_path in static_dirs:
        full_dir_path = os.path.join(base_dir, dir_path)
        os.makedirs(full_dir_path, exist_ok=True)
        # 创建.gitkeep文件
        gitkeep_path = os.path.join(full_dir_path, ".gitkeep")
        create_file(gitkeep_path)
        print(f"✅ 创建目录: {dir_path}")
    
    print(f"\n🎉 商家系统模块目录结构创建完成!")
    print(f"📍 项目根目录: {base_dir}")
    print(f"📁 总文件数: {len(structure)}")
    print(f"\n📋 下一步:")
    print("1. 配置 .env 文件中的数据库连接")
    print("2. 安装依赖: pip install -r requirements.txt")
    print("3. 初始化数据库: python scripts/init_database.py")
    print("4. 启动服务: python app/main.py")

if __name__ == "__main__":
    create_merchant_structure()