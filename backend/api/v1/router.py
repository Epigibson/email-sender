from fastapi import APIRouter, Security
from core.security import get_current_user
from api.v1.handlers.user_handlers import router as user_router
from api.v1.handlers.auth_handlers import router as auth_router
from api.v1.handlers.email_handlers import router as email_router

routerv1 = APIRouter()

routerv1.include_router(
    router=auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

routerv1.include_router(
    router=user_router,
    prefix="/users",
    tags=["Users"]
    # dependencies=[Security(get_current_user, scopes=["*:*:*"])]
)

routerv1.include_router(
    router=email_router,
    prefix="/email",
    tags=["Email"]
)

# Health check - Sin autenticación
@routerv1.get(
    "/health",
    summary="Health check",
    description="Endpoint to check if the API is up and running.",
    tags=["Health check"]
)
async def check():
    return {"API is running": "Services are healthy"}
