from pydantic import BaseModel

# 1. 用户注册时，前端传过来的数据格式
class UserCreate(BaseModel):
    username: str
    password: str

# 2. 用户登录成功后，后端返回给前端的 Token 格式
class Token(BaseModel):
    access_token: str
    token_type: str

# 3. 前端发送查询订单请求时，传过来的数据格式
class OrderQuery(BaseModel):
    order_sn: str  # 比如 "10086"

# =====================================================================
# 【核心修复：退款申请的数据格式】
# 咱们刚才的 orders.py 里用到了这个类，必须在这里定义出来。
# 前端发退款请求时，必须提供订单号和问题描述。
# =====================================================================
class RefundApply(BaseModel):
    order_sn: str
    issue_desc: str