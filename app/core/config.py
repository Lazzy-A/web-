import os
from dotenv import load_dotenv  

load_dotenv()

class Config:

    # 数据配置
    DB_USER = os.getenv("DB_USER","root")
    DB_PASSWORD = os.getenv("DB_PASSWORD","123456")
    DB_HOST = os.getenv("DB_HOST","localhost")
    DB_PORT = os.getenv("DB_PORT","3306")
    DATABASE_NAME = os.getenv("DATABASE_NAME","test")
    @property
    def DATABASE_URL(self)->str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DATABASE_NAME}"

    # JWT 配置
    SECRET_KEY : str = os.getenv("SECRET_KEY","fjds78fds90fdsjklsafd")
    ALGORITHM : str = os.getenv("ALGORITHM","HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES : int = int(os.getenv("ACCESS_TOKEN_EXPITE_MINUTES",10))

# 创建全局配置
config = Config()