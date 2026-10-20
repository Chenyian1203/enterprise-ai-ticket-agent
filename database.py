from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# =====================================================================
# 【企业重点 1：数据库连接地址】
# 为什么这么写？企业里本地测试一般用 SQLite，上生产环境直接换成 MySQL。
# 只要换掉这一行字符串，下面的所有代码都不用动，这叫"无缝切换"。
# =====================================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./enterprise.db"

# =====================================================================
# 【企业重点 2：创建数据库引擎】
# 这是整个系统的"心脏"。connect_args={"check_same_thread": False} 是专门
# 为了解决 SQLite 在多线程并发下报错的问题。企业级高并发系统必须处理这个。
# =====================================================================
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# =====================================================================
# 【企业重点 3：创建会话工厂（SessionLocal）】
# 每次前端发来请求，系统就会从这个工厂里派一个"通讯员"去数据库拿数据。
# autocommit=False 保证数据不会乱提交，autoflush=False 防止意外写入。
# =====================================================================
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# =====================================================================
# 【企业重点 4：创建基类 Base】
# 所有的数据表（User、Order、Ticket）都要继承这个 Base。
# 它就像一张图纸的底板，保证所有表都遵循统一的规范。
# =====================================================================
Base = declarative_base()

# =====================================================================
# 【企业重点 5：依赖注入（yield 生成器）】
# 这是 FastAPI 官方推荐的企业级写法。
# try...finally 保证了无论你的业务代码是正常结束还是疯狂报错，
# 最后都会执行 db.close()，100% 防止数据库连接泄漏（死机）。
# =====================================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()