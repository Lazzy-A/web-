from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user_router, product_router,order_router,category_router,inventory_router
from sqlalchemy import text

# with engine.connect()as conn:
#     conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
#     conn.commit()
# Base.metadata.drop_all(bind=engine)
# # 删除后重新启用外键检查
# with engine.connect() as conn:
#     conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
#     conn.commit()
# 创建数据库表（首次运行自动建表）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="我的Web项目", version="0.1.0")

# 注册路由
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(category_router.router)
app.include_router(inventory_router.router)
@app.get("/")
def root():
    return {"message": "服务正常运行，去 /docs 试试吧"}
