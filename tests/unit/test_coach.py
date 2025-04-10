import pytest
from openai import OpenAI

from coach import query_coach


def test_query_coach(monkeypatch, mocker):

    monkeypatch.setenv("openai_api_key", "ABC-123")

    mock_response = mocker.Mock()
    mock_response.choices = [
        mocker.Mock(message=mocker.Mock(content="Do 5km at tempo pace."))
    ]

    mock_create = mocker.patch("coach.OpenAI")
    mock_create.return_value.chat.completions.create.return_value = mock_response

    result = query_coach("Last week: 5km in 25 minutes, 10km in 55 minutes.")

    assert result == "ERROR"
