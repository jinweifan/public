""" Settings for the application """
from fastapi.security import OAuth2PasswordBearer

from base_api.utils.env import Env

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/users/login")

# MYSQL
MYSQL_USER = Env.string("MYSQL_USER", "root")
MYSQL_PASSWORD = Env.string("MYSQL_PASSWORD")
MYSQL_HOST = Env.string("MYSQL_HOST")
MYSQL_PORT = Env.int("MYSQL_PORT", 3306)
MYSQL_DATABASE = Env.string("MYSQL_DB_BASE", "base")
MYSQL_DB_URL = (
    f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/"
)
BASE_DB_URL = MYSQL_DB_URL + MYSQL_DATABASE
FANBLOG_DB_URL = MYSQL_DB_URL + "fanblog"

# REDIS
REDIS_HOST = Env.string("REDIS_HOST")
REDIS_PORT = Env.int("REDIS_PORT", 6379)
REDIS_PASSWORD = Env.string("REDIS_PASSWORD", "melon2021")
REDIS_RDVS_DB = 9
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_RDVS_DB}"

# TENCENT SMS
TENCENT_SECRET_ID = Env.string("TENCENT_SECRET_ID")
TENCENT_SECRET_KEY = Env.string("TENCENT_SECRET_KEY")
SMS_SDK_APP_ID = Env.string("SMS_SDK_APP_ID")
SIGN_NAME = Env.string("SIGN_NAME")
EXTEND_CODE = Env.string("EXTEND_CODE")
SESSION_CONTEXT = Env.string("SESSION_CONTEXT")
SENDER_ID = Env.string("SENDER_ID")
TENCET_ENDPOINT = Env.string("TENCET_ENDPOINT")
TENCENT_SIGNMETHOD = Env.string("TENCENT_SIGNMETHOD")
TENCENT_LANGUAGE = Env.string("TENCENT_LANGUAGE")
