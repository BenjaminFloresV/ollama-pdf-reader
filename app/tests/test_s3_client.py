import importlib
from unittest.mock import MagicMock, patch
import pytest
import pytest_asyncio


@pytest.fixture(autouse=True)
def reload_s3_module(monkeypatch):
    """Reload the s3_client module before each test to ensure clean state."""
    module = importlib.import_module("app.storage.s3_client")
    # Reset globals
    monkeypatch.setattr(module, "s3_client", None)
    yield module


def test_get_s3_client_without_init_raises(reload_s3_module):
    with pytest.raises(RuntimeError):
        reload_s3_module.get_s3_client()


def test_init_s3_client_sets_global(reload_s3_module):
    # Arrange
    dummy_boto_client = MagicMock(name="boto3_client")

    with patch("app.storage.s3_client.boto3.client", return_value=dummy_boto_client) as mocked:
        # Act
        reload_s3_module.init_s3_client()

    # Assert
    mocked.assert_called_once()
    assert reload_s3_module.s3_client is dummy_boto_client
    assert reload_s3_module.get_s3_client() is dummy_boto_client


@pytest_asyncio.fixture
async def dummy_s3_env(monkeypatch, reload_s3_module):
    """Prepare mocked S3 client and bucket for async tests."""
    dummy_body = MagicMock()
    dummy_body.read.return_value = b"hello world"

    dummy_client = MagicMock()
    dummy_client.get_object.return_value = {"Body": dummy_body}

    # Patch global client and bucket name
    monkeypatch.setattr(reload_s3_module, "s3_client", dummy_client)
    monkeypatch.setattr(reload_s3_module, "AWS_BUCKET_NAME", "unit-test-bucket")
    yield dummy_client, reload_s3_module


@pytest.mark.asyncio
async def test_download_bucket_object_returns_bytes(dummy_s3_env):
    dummy_client, module = dummy_s3_env

    data = await module.download_bucket_object("file.txt")

    dummy_client.get_object.assert_called_once_with(Bucket="unit-test-bucket", Key="file.txt")
    assert data == b"hello world"
