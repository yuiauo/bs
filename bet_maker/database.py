import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import dotenv

dotenv.load_dotenv()

url = os.getenv("PG_DATABASE_URL")


bind = create_async_engine(url=url, future=True, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=bind, expire_on_commit=False)
