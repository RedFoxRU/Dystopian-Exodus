import pytest

from unittest.mock import AsyncMock
from handlers.client import searchCommand


@pytest.mark.asyncio
async def test_echo_handler():
    text_mock = "test123"
    message_mock = AsyncMock(text=text_mock)
    state = AsyncMock(text=text_mock)
    await searchCommand(message=message_mock, state=state)
    print(message_mock.answer.assert_called_with(text_mock, state))