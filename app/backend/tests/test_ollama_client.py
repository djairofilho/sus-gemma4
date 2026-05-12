import json

import httpx
import pytest

from app.ollama_client import OllamaClient, OllamaError


@pytest.mark.anyio
async def test_ollama_client_posts_generate_request() -> None:
    captured_payload: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured_payload.update(json.loads(request.content.decode()))
        return httpx.Response(200, json={"response": "resposta estruturada"})

    transport = httpx.MockTransport(handler)

    client = OllamaClient("http://localhost:11434/", "gemma-test", 3, transport)

    response = await client.generate("prompt SUS")

    assert response == "resposta estruturada"
    assert captured_payload == {"model": "gemma-test", "prompt": "prompt SUS", "stream": False}


@pytest.mark.anyio
async def test_ollama_client_raises_on_http_failure() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, request=request)

    transport = httpx.MockTransport(handler)

    client = OllamaClient("http://localhost:11434", "gemma-test", 3, transport)

    with pytest.raises(OllamaError):
        await client.generate("prompt SUS")


@pytest.mark.anyio
async def test_ollama_client_raises_on_empty_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"response": ""}, request=request)

    transport = httpx.MockTransport(handler)

    client = OllamaClient("http://localhost:11434", "gemma-test", 3, transport)

    with pytest.raises(OllamaError):
        await client.generate("prompt SUS")
