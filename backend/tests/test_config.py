import pytest

from app.core.config import Settings, check_required_secrets


@pytest.mark.parametrize("value", ["", "changeme", "  "])
def test_weak_jwt_secret_fails(value):
    with pytest.raises(RuntimeError):
        check_required_secrets(Settings(jwt_secret=value))


def test_strong_jwt_secret_passes():
    check_required_secrets(Settings(jwt_secret="x" * 64))
