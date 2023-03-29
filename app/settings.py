"""
@Project  : nucleic
@Author   : QiaoPengjun
@Time     : 2023/3/28 23:34
@Software : PyCharm
@File     : settings.py
"""
from fastapi.security import OAuth2PasswordBearer
from urllib import parse

# 定义配置项
# JWT 密钥，使用命令 openssl rand -hex 32 生成
JWT_SECRET_KEY = 'ed48426ad562bc9fc5026a19cf4b3565a43697fe4dd5e3bbd4adbfcc98396455'
JWT_ALGORITHM = 'HS256'  # 加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # JWT中Token的有效期
AUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl="auth/login")  # 身份认证设置
AUTH_INIT_USER = 'admin'
AUTH_INIT_PASSWORD = '111111'

# 数据库配置
DB_HOST = 'localhost'  # 运行数据库服务的主机名或IP地址
DB_USERNAME = 'root'  # 访问数据库的用户名
DB_PASSWORD = parse.quote('12345678')
DB_DATABASE = 'nucleic'  # 数据库名
