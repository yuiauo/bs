from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import settings


bind = create_async_engine(url=settings.env.PG_DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(bind=bind, expire_on_commit=False)
