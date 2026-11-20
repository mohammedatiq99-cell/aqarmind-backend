import pytest
from fastapi import HTTPException

from app.core.guardrails import validate_user_message


def test_message_is_trimmed():
    assert validate_user_message('  Show two-bedroom properties  ') == 'Show two-bedroom properties'


def test_blank_message_rejected():
    with pytest.raises(HTTPException) as exc:
        validate_user_message('  ')
    assert exc.value.status_code == 422


def test_oversized_message_rejected():
    with pytest.raises(HTTPException) as exc:
        validate_user_message('x' * 6001)
    assert exc.value.status_code == 413
