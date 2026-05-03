from unittest.mock import Mock, patch

from netcorex_modelswitch.providers.openai_provider import OpenAIProvider


@patch("netcorex_modelswitch.providers.openai_provider.requests.post")
def test_openai_provider_maps_response(mock_post):
    response = Mock()
    response.json.return_value = {
        "model": "gpt-5-mini",
        "choices": [{"message": {"content": "Resposta premium"}}],
        "usage": {"prompt_tokens": 15, "completion_tokens": 25},
    }
    response.raise_for_status.return_value = None
    mock_post.return_value = response

    provider = OpenAIProvider(api_key="token")
    result = provider.execute("teste", model="gpt-5-mini")

    assert result.provider == "openai"
    assert result.model == "gpt-5-mini"
    assert result.content == "Resposta premium"
    assert result.input_tokens == 15
    assert result.output_tokens == 25
