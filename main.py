import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # 导入跨域资源共享安全中间件
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse  # 导入URL地址重定向响应类
from app.database import generate_tables  # 导入自定义app包里的数据库表生成函数
from app.settings import AUTH_SCHEMA  # 导入自定义app包里的身份认证设置
from auth.router import route as auth_router  # 导入自定义 auth 包里的路由模块
from auth.services import init_admin_user  # 导入自定义auth包里创建新用户的 admin_user 函数
from checkin.router import route as checkin_router  # 导入自定义 checkin 包里的路由模块
from person.router import route as person_router  # 导入自定义 person 包里的路由模块

app = FastAPI()
# 中间件设置，用于配置跨域属性的中间件
origins = [  # 定义可用域列表
    "http://localhost:8000",  # 后端应用使用的端口
    "http://localhost:8080",  # 前端应用使用的端口
]
app.add_middleware(
    CORSMiddleware,  # 内置中间件类
    allow_origins=origins,  # 参数1 可用域列表
    allow_credentials=True,  # 参数 2 允许使用 cookie，设置值 True
    allow_methods=["*"],  # 参数 3 允许的方法，全部
    allow_headers=["*"],  # 参数 4 允许的 Header，全部
)

# 注册应用路由，每个路由对应一个模块
app.include_router(
    checkin_router,  # 注册登记模块
    prefix='/checkin',  # 设置路由的前缀路径
    dependencies=[Depends(AUTH_SCHEMA)]  # 使用应用依赖的方式增加身份认证
)
app.include_router(person_router, prefix='/person')
app.include_router(auth_router, prefix='/auth')
# 注册静态资源文件，将前端后端项目整合运行
# app.mount('/web', StaticFiles(directory='web/dist'), 'web')  # 管理端页面项目
# app.mount('/h5', StaticFiles(directory='h5/dist'), 'h5')  # 移动端项目


# 定义根路由路径指向的页面
@app.get('/')
def toweb():
    return RedirectResponse('/web/index.html')


# 生成表结构，SQLAlchemy 的数据表同步工具
generate_tables()

# 创建初始管理员账号
init_admin_user()
# 项目入口文件
if __name__ == '__main__':
    uvicorn.run(app=app)
