from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.config import config

# 数据库连接配置
DB_USER = config.DB_USER    
DB_PASSWORD = config.DB_PASSWORD    
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DATABASE_NAME = config.DATABASE_NAME    
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE_NAME}"   


def ensure_database_exists():
    try:
        # 尝试连接到数据库
        test_engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE_NAME}"
        )
        with test_engine.connect() as connection:
            # 如果连接成功，说明数据库存在
            print(f"Database '{DATABASE_NAME}' exists.")    
            return test_engine
    except OperationalError as e:
        if "Unknown database" in str(e):
            # 数据库不存在，创建数据库
            print(f"数据库 '{DATABASE_NAME}' 不存在，正在创建...")
            with create_engine(
                f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
            ).connect() as connection:
                connection.execute(text(f"CREATE DATABASE {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))    
                print(f"数据库 '{DATABASE_NAME}' 创建成功。")   
                return create_engine(
                    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE_NAME}"
                )
        else:
            # 其他连接错误，抛出异常
            raise e

engine = ensure_database_exists()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

