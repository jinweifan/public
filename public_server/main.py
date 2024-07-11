""" fastapi 主文件"""
from typing import Any, Optional

import sqlalchemy
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from public_server import api
from public_server.schemas.response_info import RSINFO, NMCException, RespInfo, RFInfo

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api.router)


async def startup():
    """启动时加载"""
    # await create_base_tables()
    ...


async def shutdown():
    """关闭时处理"""
    # await base_engine.dispose()
    ...


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    """index"""
    return "<h1 align='center'>Welcome To Base API</h1>"


def use_route_names_as_operation_ids(application: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in application.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)


def response_for_error(
    error: Any,
    exception: Optional[Exception] = None,
    request: Optional[Request] = None,
) -> Response:
    """创建错误响应,并包含错误信息。

    Args:
         error: 引发的错误。如果这是``None``，则不会返回错误信息。
         exception: 引发的异常。如果这是``None``，则不会返回异常信息。
         request: 导致错误的请求。如果这是无

    Returns:
        JSONResponse: 包含错误信息的响应。
    """
    if isinstance(error, RespInfo):
        if exception is not None:
            # 使用error format exception
            msg = f"{exception.__class__.__name__}: {exception}"
            error = RSINFO.REQUEST_VALIDATION_ERROR.with_message(msg)

        if request is not None:
            pass
            # request.state.log_data[error.reason] = error.message

        return JSONResponse(
            {"code": error.code, "reason": error.reason, "message": error.message},
            status_code=error.http_status,
        )
    else:
        return JSONResponse(
            {"code": 0, "reason": str(error), "message": str(error)
             }
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, e: RequestValidationError):
    """请求验证异常处理"""
    return response_for_error(RSINFO.REQUEST_VALIDATION_ERROR)


@app.exception_handler(AssertionError)
async def assert_exception_handler(request: Request, exc: AssertionError):
    """断言异常处理"""
    return response_for_error(RFInfo.FAILED.with_message(message=str(exc)))


@app.exception_handler(NMCException)
async def http_exception_handler(request: Request, exc: NMCException):
    """断言异常处理"""
    return response_for_error(exc.error)


@app.exception_handler(sqlalchemy.exc.IntegrityError)
async def integrity_exception_handler(request: Request, exc: sqlalchemy.exc.IntegrityError):
    """数据库错误常处理"""
    if exc.code == 'gkpj':
        return response_for_error(RFInfo.FAILED.with_message(message='数据已存在', reason="data exist"))
    raise exc
