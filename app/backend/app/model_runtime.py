from typing import Protocol


class ModelRuntime(Protocol):
    async def generate(self, prompt: str) -> str:
        """Generate model text from a prompt."""
