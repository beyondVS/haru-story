from litestar import Litestar, asgi
from litestar.config.cors import CORSConfig
from litestar.types import Receive, Scope, Send
from strawberry.asgi import GraphQL

from haru_backend.api.graphql.schema import schema
from haru_backend.api.http.health import health
from haru_backend.infrastructure.database.config import database

graphql_app = GraphQL(schema, graphql_ide=None, allow_queries_via_get=False)


@asgi("/graphql", is_mount=True, copy_scope=True)
async def graphql(scope: Scope, receive: Receive, send: Send) -> None:
    await graphql_app(scope, receive, send)


app = Litestar(
    route_handlers=[health, graphql],
    plugins=[database],
    cors_config=CORSConfig(
        allow_origins=["http://tauri.localhost", "tauri://localhost"],
        allow_methods=["POST"],
        allow_headers=["Content-Type"],
    ),
)
