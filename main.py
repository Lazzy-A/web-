from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import user_router, product_router,order_router,category_router,inventory_router,supplier_router,brand_router,warehouse_router,dashboard_router
from sqlalchemy import text
from app.core.exceptions import register_exceptions_handler
from app.core.logger import logger
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin()as conn:
        await conn.run_sync(Base.metadata.create_all)
        print ("Database tables created.")

        yield

        await engine.dispose()
        print("Database connection pool closed.")

app = FastAPI(lifespan=lifespan,title="我的Web项目", version="0.1.0")
# 注册全局异常处理器
register_exceptions_handler(app)

    
# 注册路由
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(category_router.router)
app.include_router(inventory_router.router)
app.include_router(supplier_router.router)
app.include_router(brand_router.router)
app.include_router(warehouse_router.router)
app.include_router(dashboard_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
