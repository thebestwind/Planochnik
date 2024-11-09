import pytest
from unittest.mock import patch, MagicMock
from handlers import send_welcome
from telebot.types import Message, User


@pytest.fixture
def mock_bot():
    with patch('handlers.bot') as mock_bot:
        yield mock_bot


def test_start_command(mock_bot):
    # Создаем объект сообщения и его отправителя
    message = MagicMock(spec=Message)
    message.text = "/start"
    message.from_user = MagicMock(spec=User)
    message.from_user.username = "test_user"
    message.from_user.first_name = "Test"
    message.from_user.last_name = "User"

    # Вызываем функцию send_welcome
    send_welcome(message)

    # Проверяем, что бот отправляет правильный ответ
    mock_bot.reply_to.assert_called_once_with(message, "Время подкачаться! \nВведи количество упражнений. От 1 до 10")