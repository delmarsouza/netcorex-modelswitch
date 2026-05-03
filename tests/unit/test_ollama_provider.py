from unittest.mock import Mock, patch

from netcorex_modelswitch.providers.ollama import OllamaProvider


@patch("netcorex_modelswitch.providers.ollama.requests.post")
def test_ollama_provider_maps_response(mock_post):
    response = Mock()
    response.json.return_value = {
        "response": "Olá mundo",
        "model": "qwen2.5:14b",
        "prompt_eval_count": 12,
        "eval_count": 20,
    }
    response.raise_for_status.return_value = None
    mock_post.return_value = response

    provider = OllamaProvider()
    result = provider.execute("teste", model="qwen2.5:14b")

    assert result.provider == "ollama"
    assert result.model == "qwen2.5:14b"
    assert result.content == "Olá mundo"
    assert result.input_tokens == 12
    assert result.output_tokens == 20
