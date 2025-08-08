from beanie import init_beanie
from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from models.user_model import User


# Create async client to connect to the database.
client = AsyncIOMotorClient(host=settings.DATABASE_URL)


async def init_db():
    """ Create database connection and configure special settings.

    :return: Database connection.
    """
    # Configure database indexes or special settings.
    # Must specify database model(s) to configure.
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            User
        ]
    )
