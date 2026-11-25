from os import getenv

import pytest
from litestar.testing import AsyncTestClient
from sqlalchemy import text

from haru_backend.app import app
from haru_backend.infrastructure.database.config import database_config


@pytest.mark.anyio
async def test_postgresql(anyio_backend: str) -> None:
    if getenv("HARU_TEST_DATABASE") != "1":
        pytest.skip("Set HARU_TEST_DATABASE=1 to check local PostgreSQL")

    async with AsyncTestClient(app):
        engine = database_config.provide_engine(app.state)
        async with engine.connect() as connection:
            assert await connection.scalar(text("SELECT 1")) == 1


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
