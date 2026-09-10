from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logger import logger

# 统一响应格式
def build_response(code :int,message:str,data=None):
    return{
        "code":code,
        "message":message,
        "data":data 
    }

# 注册异常处理器
def register_exceptions_handler(app:FastAPI):
    # 处理HTTP异常
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
    ):
        logger.error(f"HTTP异常: {exc.status_code} {exc.detail}")
        return JSONResponse(status_code=exc.status_code,content=build_response(exc.status_code,exc.detail))
    # 处理请求参数异常
    @app.exception_handler(RequestValidationError)
    async def vaildation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        errors = [{
            "field": e("loc")[-1],
            "message": e("msg")
        } for e in exc.errors()]
        logger.error(f"请求参数异常: {exc.errors()}")   
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,content=build_response(status.HTTP_422_UNPROCESSABLE_ENTITY,errors)) 
    # 处理其他异常
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception
    ):
        logger.error(f"未处理的异常: {exc}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content=build_response(status.HTTP_500_INTERNAL_SERVER_ERROR,"服务器内部错误"))
    