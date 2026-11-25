from litestar import get


@get("/health", sync_to_thread=False)
def health() -> dict[str, str]:
    return {"status": "ok"}
