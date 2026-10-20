from routers import users, orders, chat
from fastapi import FastAPI
from database import engine, Base, SessionLocal
import models
import auth

# 1. 建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="企业级 AI 工单中台 API", version="1.0.0")

# 2. 挂载路由（关键：必须把 users 和 orders 都挂上去）
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(chat.router)

# 3. 启动时初始化数据
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    
    # 强行生成 admin 账号
    if db.query(models.User).filter(models.User.username == "admin").count() == 0:
        admin_user = models.User(
            username="admin", 
            hashed_password=auth.get_password_hash("123456"), 
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ 管理员账号 admin 已自动创建！")
        
    # 塞入测试订单
    if db.query(models.Order).count() == 0:
        order1 = models.Order(order_sn="10086", product_name="iPhone 15", amount=5999.0, status="已发货")
        order2 = models.Order(order_sn="10087", product_name="MacBook Pro", amount=12999.0, status="待发货")
        db.add(order1)
        db.add(order2)
        db.commit()
        print("✅ 测试订单已写入！")
        
    db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Enterprise AI Platform API!"}