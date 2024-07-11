"""响应模型"""
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from public_server.schemas.response_info import RSINFO


T = TypeVar("T")


class RespModel(BaseModel, Generic[T]):
    """HTTP response model."""

    code: int = RSINFO.OK.code
    reason: Optional[str] = RSINFO.OK.reason
    message: Optional[str] = RSINFO.OK.message
    data: Optional[T] = None
