from app.main import app


if __name__ == '__main__':
    import uvicorn

    from app.core.config import get_settings

    settings = get_settings()
    uvicorn.run(
        'app.main:app',
        host=settings.backend_host,
        port=settings.backend_port,
        reload=False,
    )
