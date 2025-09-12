
import pytest

from app.utils.toolbelt import validate_rut


@pytest.mark.parametrize("rut, expected", [
    ("12345678-9", False),
    ("20217260-1", True),
    ("20.217.260-1", True),
    ("13008100-2", True),
    ("13.008.100-2", True),
    ("10032779-4", False),
    ("RIT 4972 - 2025", False),
])
def test_validate_ruts(rut, expected):
    assert validate_rut(rut) == expected

