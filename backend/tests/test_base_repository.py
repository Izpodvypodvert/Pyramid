import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Field, select, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.utils.repository import SQLModelRepository
from app.core.config import settings


DATABASE_URL = settings.test_database_url


class BaseModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    is_published: bool = False


@pytest_asyncio.fixture
async def repo():
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        repository = SQLModelRepository(session=session)
        repository.model = BaseModel
        yield repository
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def test_insert_data(repo: SQLModelRepository):

    entity = await repo.insert_data(
        title="Test Title",
        description="Test Description",
        is_published=True,
    )
    await repo.session.commit()
    await repo.session.close()

    assert entity.title == "Test Title"


async def test_find_one_or_none_existing(repo: SQLModelRepository):
    # Insert data into the database for testing
    entity = await repo.insert_data(
        title="Unique Title", description="Unique Description", is_published=False
    )
    await repo.session.commit()

    # Try to find the entity we just inserted
    found_entity = await repo.find_one_or_none(title="Unique Title")
    await repo.session.close()

    assert found_entity is not None
    assert found_entity.id == entity.id


async def test_find_one_or_none_non_existing(repo: SQLModelRepository):
    # Try to find a non-existing entity
    found_entity = await repo.find_one_or_none(title="Non Existing Title")
    await repo.session.close()

    assert found_entity is None


async def test_find_all_with_filter(repo: SQLModelRepository):
    # Insert multiple entities
    await repo.insert_data(
        title="Test", description="Test Description 1", is_published=True
    )
    await repo.insert_data(
        title="Test", description="Test Description 2", is_published=False
    )
    await repo.session.commit()

    # Fetch all entities with the title "Test"
    entities = await repo.find_all(title="Test")
    await repo.session.close()

    assert len(entities) == 2


async def test_find_all_without_filter(repo: SQLModelRepository):
    # Fetch all entities
    entities = await repo.find_all()
    await repo.session.close()

    # Assuming no other entities are present from previous tests
    assert isinstance(entities, list)


async def test_update_fields_by_id(repo: SQLModelRepository):
    # Insert an entity and update it
    entity = await repo.insert_data(
        title="Old Title", description="Old Description", is_published=False
    )
    await repo.session.commit()

    rows_updated = await repo.update_fields_by_id(entity.id, title="New Title")
    await repo.session.commit()

    # Fetch the updated entity
    updated_entity = await repo.find_one_or_none(id=entity.id)
    await repo.session.close()

    assert rows_updated == 1
    assert updated_entity.title == "New Title"


async def test_delete(repo: SQLModelRepository):
    # Insert an entity and then delete it
    entity = await repo.insert_data(
        title="To Delete", description="To Delete Description", is_published=True
    )
    await repo.session.commit()

    rows_deleted = await repo.delete(title="To Delete")
    await repo.session.commit()

    # Verify the entity is deleted
    deleted_entity = await repo.find_one_or_none(title="To Delete")
    await repo.session.close()

    assert rows_deleted == 1
    assert deleted_entity is None
