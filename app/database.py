from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import text,create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base,sessionmaker
from app.core.config import config

# 配置
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DATABASE_NAME = config.DATABASE_NAME

# 异步连接字符串（注意是 aiomysql）
ASYNC_DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE_NAME}"

# 同步连接字符串（仅用于启动时检查数据库是否存在）
SYNC_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE_NAME}"


def ensure_database_exists():
    """
    检查数据库是否存在，不存在就创建。
    这个函数只在启动时执行一次，用同步方式就够了，不用改成 async。
    """
    try:
        # 先尝试连接目标数据库
        test_engine = create_engine(SYNC_DATABASE_URL)
        with test_engine.connect() as connection:
            print(f"Database '{DATABASE_NAME}' exists.")
            test_engine.dispose()
            return
    except OperationalError as e:
        if "Unknown database" not in str(e):
            raise e

    # 数据库不存在，创建它
    print(f"数据库 '{DATABASE_NAME}' 不存在，正在创建...")
    base_engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
    )
    with base_engine.connect() as connection:
        connection.execute(
            text(
                f"CREATE DATABASE {DATABASE_NAME} "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
        )
        connection.commit()
    base_engine.dispose()
    print(f"数据库 '{DATABASE_NAME}' 创建成功。")


# 应用启动时先检查数据库
ensure_database_exists()

sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=sync_engine)

# 创建异步引擎
engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close