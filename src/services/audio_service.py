import httpx
from src.config.config import Config


class AudioService:

    def __init__(self, config: Config):
        self.config = config

    async def transcribe(self, file_url: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.STT_API_KEY}",
        }

        payload = {
            "model": self.config.STT_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "audio_url", "audio_url": {"url": file_url}},
                        {"type": "text", "text": "直接转录为文本"},
                    ],
                }
            ],
            "max_tokens": 500,
            "presence_penalty": 0.1,
            "frequency_penalty": 0.2,
            "stream": False,
        }

        timeout = httpx.Timeout(
            connect=5.0,
            read=60.0,
            write=10.0,
            pool=5.0,
        )

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url=self.config.STT_API_URL,
                headers=headers,
                json=payload,
            )

        response.raise_for_status()

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Invalid STT response format: {data}") from e
