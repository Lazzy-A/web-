import sys
from loguru import logger

# 移除默认的日志处理器
logger.remove()

# 添加自定义日志格式
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",level="DEBUG")

# 日志写入文件
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {file}:{line} - {message}",
    level="INFO"
)

# 将logger暴露给其他模块使用
__all__ = ["logger"]