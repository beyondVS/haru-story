from litestar.testing import TestClient

from haru_backend.app import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_graphql_service_status() -> None:
    with TestClient(app) as client:
        response = client.post("/graphql", json={"query": "{ serviceStatus }"})

    assert response.status_code == 200
    assert response.json() == {"data": {"serviceStatus": "ok"}}


def test_desktop_graphql_preflight() -> None:
    with TestClient(app) as client:
        response = client.options(
            "/graphql",
            headers={
                "Origin": "http://tauri.localhost",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

    assert response.status_code == 204 or response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://tauri.localhost"
