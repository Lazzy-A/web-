from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user_router, product_router,order_router,category_router,inventory_router,supplier_router,brand_router,warehouse_router
from sqlalchemy import text
from app.core.exceptions import register_exceptions_handler
from app.core.logger import logger

# 创建数据库表（首次运行自动建表）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="我的Web项目", version="0.1.0")
# 注册全局异常处理器
register_exceptions_handler(app)
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 项目启动成功！")
    
# 注册路由
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(category_router.router)
app.include_router(inventory_router.router)
app.include_router(supplier_router.router)
app.include_router(brand_router.router)
app.include_router(warehouse_router.router)
@app.get("/")
def root():
    return {"message": "服务正常运行，去 /docs 试试吧"}
