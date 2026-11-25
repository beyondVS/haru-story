from os import getenv

from advanced_alchemy.extensions.litestar import SQLAlchemyAsyncConfig, SQLAlchemyPlugin

database_config = SQLAlchemyAsyncConfig(
    connection_string=getenv(
        "HARU_DATABASE_URL",
        "postgresql+asyncpg://haru:haru@127.0.0.1:54329/haru_story",
    ),
)
database = SQLAlchemyPlugin(config=database_config)
