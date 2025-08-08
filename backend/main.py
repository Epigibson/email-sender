import uvicorn
from mangum import Mangum
from fastapi import FastAPI, Request
from starlette import status
from depends.db import init_db
from core.config import settings
from api.v1.router import routerv1
from contextlib import asynccontextmanager
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError


__version__ = "1.0.0"


def get_application():

    tags_metadata = [
        
    ]

    _app = FastAPI(
        title="Ricardo Minor | API Cradora de correos temporales aleatorios",
        description="API para la creación de correos temporales aleatorios",
        contact={
            "email": "hackminor@live.com.mx",
            "name": "Ricardo Minor",
            "url": "https://github.com/ricardo-minor"
        },
        openapi_tags=tags_metadata,
        version=__version__,
        docs_url=f"{settings.API_PREFIX}/docs",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        lifespan=lifespan
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin)
            for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB.
    await init_db()
    print("Init dbs...")
    yield

app = get_application()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """ Function to modify validation exception.

    :param request: HTTPRequest to handle.
    :param exc: Current validaiton error
    """
    errors = list()
    for error in exc.errors():
        try:
            field = error.get("loc")[1]
        except IndexError:
            field = None

        errors.append({
            "location": error.get("loc")[0],
            "field": field,
            "message": error.get("msg").capitalize(),
            "type": error.get("type")
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        # content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        content=jsonable_encoder({"detail": errors, "body": exc.body}),
    )

@app.get("/", summary="Welcome message", description="Endpoint to check if the API is running.", tags=["Welcome message"])
async def check():
    return {"Bienvenid@ a la API de creación de correos temporales aleatorios": "API Funcionando correctamente"}

# Include the main router.
app.include_router(router=routerv1, prefix=settings.API_PREFIX)


def lambda_handler(event, context):
    """ Mangum lambda handler.

    :param dict event: AWS Lambda event.
    :param dict context: AWS Lambda context.
    :return: Handler.
    """

    asgi_handler = Mangum(app)
    response = asgi_handler(
        event, context
    )  # Call the instance with the event arguments

    return response


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
