import os
import uuid
import pytest
import pytest_asyncio

# pytest-asyncio is required for async tests
#pytest_plugins = ("pytest_asyncio", "pytest")

# Patch the MONGO_URI used inside the MongoDBClient module **before** importing it
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")

from importlib import reload

# Re-import the module so that the patched env var is picked up
from app.persistence import mongodb as mongodb_module
mongodb_module.MONGO_URI = os.getenv("MONGO_URI")
reload(mongodb_module)  # make sure the constant is refreshed

from app.persistence.mongodb import MongoDBClient
from bson import ObjectId


@pytest_asyncio.fixture
async def mongo_client():
    """Provide an initialised MongoDBClient and ensure test DB cleanup."""
    client = MongoDBClient()
    # Name a dedicated test database so we don't accidentally mess with real data
    test_db_name = f"test_db_{uuid.uuid4().hex}"
    yield client, test_db_name
    # -------- cleanup -------- (same event loop)
    if client.client is not None:
        try:
            await client.client.drop_database(test_db_name)
            await client.client.close()
        except Exception:
            pass  # ignore cleanup issues


@pytest.mark.asyncio
async def test_insert_and_find_one(mongo_client):
    client, db_name = mongo_client
    collection = "items"

    doc_id = ObjectId()
    doc = {"_id": doc_id, "name": "Alice", "value": 10}

    # Insert
    insert_result = await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="insert_one",
        document=doc,
    )
    assert insert_result.acknowledged is True
    assert insert_result.inserted_id == doc_id

    # Find
    found_doc = await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="find_one",
        filter={"_id": doc_id},
    )
    assert found_doc is not None
    assert found_doc["name"] == "Alice"
    assert found_doc["value"] == 10


@pytest.mark.asyncio
async def test_update_and_count(mongo_client):
    client, db_name = mongo_client
    collection = "items"

    # Insert a doc to update
    doc_id = ObjectId()
    await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="insert_one",
        document={"_id": doc_id, "name": "Bob", "value": 5},
    )

    # Update
    update_result = await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="update_one",
        filter={"_id": doc_id},
        update={"$set": {"value": 15}},
        upsert=False,
    )
    assert update_result.modified_count == 1

    # Count documents with value 15
    count = await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="count_documents",
        filter={"value": 15},
    )
    assert count == 1


@pytest.mark.asyncio
async def test_find_with_pagination(mongo_client):
    client, db_name = mongo_client
    collection = "paginated"

    # Insert 12 docs
    docs = [{"_id": ObjectId(), "index": i} for i in range(12)]
    for doc in docs:
        await client.mongo_safe_query(
            database=db_name,
            collection=collection,
            function="insert_one",
            document=doc,
        )

    # Retrieve with pagination (limit 5)
    results = await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="find_with_pagination",
        limit=5,
    )
    assert isinstance(results, list)
    assert len(results) == 12


@pytest.mark.asyncio
async def test_delete_one(mongo_client):
    client, db_name = mongo_client
    collection = "delete_test"

    doc_id = ObjectId()
    await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="insert_one",
        document={"_id": doc_id, "flag": True},
    )

    del_result = await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="delete_one",
        filter={"_id": doc_id},
    )
    #print(del_result)
    assert del_result.deleted_count == 1

    # Confirm deletion
    remaining = await client.mongo_safe_query(
        database=db_name,
        collection=collection,
        function="find_one",
        filter={"_id": doc_id},
    )
    assert remaining == {}
