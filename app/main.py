from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.adapters.rest import product_rest
from app.config import VERSION

app = FastAPI(title="Stream Community Products", version=VERSION)
app.include_router(product_rest.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=VERSION,
        description="Stream Community Products",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
