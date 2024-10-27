import os

import dotenv
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bet_maker.main import app as bapp
from bet_maker.models import Base
from bet_maker.services import get_db


dotenv.load_dotenv()
TEST_DATABASE_URL = os.getenv("PG_DATABASE_URL")

bind = create_async_engine(url=TEST_DATABASE_URL, future=True, echo=True)
TestingSession = async_sessionmaker(bind=bind)


async def override_get_db():
    db = TestingSession()
    try:
        yield db
    except Exception:
        await db.rollback()
    finally:
        await db.close()


@pytest_asyncio.fixture(loop_scope="session")
async def run_fake_db():
    async with bind.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with bind.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await bind.dispose()


# noinspection PyUnresolvedReferences
bapp.dependency_overrides[get_db] = override_get_db
