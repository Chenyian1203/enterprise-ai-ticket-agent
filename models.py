from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from database import Base

# =====================================================================
# 【企业重点 1：用户表】
# 用于存储登录账号。注意：密码绝对不能存明文，存的是 hashed_password。
# =====================================================================
class User(Base):
    __tablename__ = "users"  # 数据库里的表名

    id = Column(Integer, primary_key=True, index=True)  # 主键，自动递增，加索引查得快
    username = Column(String(50), unique=True, index=True) # 用户名唯一
    hashed_password = Column(String(255))                  # 加密后的密码
    is_admin = Column(Boolean, default=False)              # 权限控制，默认不是管理员

# =====================================================================
# 【企业重点 2：订单表】
# 模拟真实的电商订单，客服系统查库全靠它。
# =====================================================================
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_sn = Column(String(50), unique=True, index=True) # 订单号（如 10086）
    product_name = Column(String(100))                     # 商品名称
    amount = Column(Float)                                 # 金额
    status = Column(String(20), default="已发货")          # 订单状态

# =====================================================================
# 【企业重点 3：工单表】
# 客服系统里最核心的表。AI 建的每一张退款单，都会变成这里的一条记录。
# =====================================================================
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    # 【外键】绑定订单表，说明这个工单属于哪一笔订单
    order_id = Column(Integer, ForeignKey("orders.id"))
    issue_desc = Column(String(255))                 # 客户反馈的问题描述
    status = Column(String(20), default="待审核")    # 工单状态（待审核、已退款）