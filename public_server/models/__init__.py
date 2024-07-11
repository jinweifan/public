""" 数据库模型初始化 """
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# from base_api.models.user import Base
# from base_api.settings import BASE_DB_URL, FANBLOG_DB_URL

# base_engine = create_async_engine(BASE_DB_URL, echo=False)
# vanblog_engine = create_async_engine(FANBLOG_DB_URL, echo=False)

# base_async_session = async_sessionmaker(base_engine, expire_on_commit=False)
# vanblog_async_session = async_sessionmaker(vanblog_engine, expire_on_commit=False)


# async def create_base_tables():
#     """创建base库的表"""
#     async with base_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def create_fanblog_tables():
#     """创建fanblog的表"""
#     async with vanblog_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
