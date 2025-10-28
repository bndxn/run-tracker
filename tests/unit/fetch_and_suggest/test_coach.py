"""Tests functions in fetch_and_suggest.coach.py."""

from fetch_and_suggest.coach_and_formatter import query_coach


def test_query_coach(monkeypatch, mocker):
    """Checks the coach function works as expected using a mock OpenAI response."""
    monkeypatch.setenv("OPENAI_API_KEY", "ABC-123")

    mock_response = mocker.Mock()
    mock_response.choices = [
        mocker.Mock(message=mocker.Mock(content="Do 5km at tempo pace."))
    ]

    mock_create = mocker.patch("fetch_and_suggest.coach_and_formatter.OpenAI")
    mock_create.return_value.chat.completions.create.return_value = mock_response

    result = query_coach("Last week: 5km in 25 minutes, 10km in 55 minutes.")

    assert result == "Do 5km at tempo pace."
