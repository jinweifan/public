"""数据库依赖注入"""
# from typing import AsyncGenerator

# import aioredis

# from base_api.settings import REDIS_URL


# async def redis_pool() -> aioredis.Redis:
#     """得到redis连接池"""
#     pool = aioredis.ConnectionPool.from_url(
#         REDIS_URL, max_connections=10, decode_responses=True
#     )
#     return await aioredis.Redis(connection_pool=pool)


# async def get_redis() -> AsyncGenerator:
#     """获取redis连接池"""
#     redis = await redis_pool()
#     yield redis
#     await redis.close()
