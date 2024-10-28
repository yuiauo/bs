import os

import dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


dotenv.load_dotenv()
PG_DATABASE_URL = os.getenv("PG_DATABASE_URL")

bind = create_async_engine(url=PG_DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(bind=bind, expire_on_commit=False)
