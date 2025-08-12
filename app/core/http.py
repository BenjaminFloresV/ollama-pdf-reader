
import httpx
from typing import Optional, Union

from app.core.config import DEFAULT_HTTP_TIMEOUT

class AsyncHTTPFetcher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncHTTPFetcher, cls).__new__(cls)
            cls._instance._client = httpx.AsyncClient()
        return cls._instance
    
    async def handle_response(self, response: httpx.Response, response_type: Optional[str] = "json") -> Optional[str]:
        if response_type == "json":
            return response.json()
        elif response_type == "text":
            return response.text
        else:
            return response.text

    @classmethod
    async def close_client(cls):
        if cls._instance is not None and cls._instance._client is not None:
            await cls._instance._client.aclose()
            cls._instance._client = None

    async def post(
        self, url: str,
        data: Union[dict, list, str],
        headers: Optional[dict] = None,
        timeout: Optional[int] = DEFAULT_HTTP_TIMEOUT,
        response_type: Optional[str] = "json"
    ):
        try:
            response = await self._instance._client.post(url, json=data, headers=headers, timeout=timeout)
            response.raise_for_status()
            return await self.handle_response(response, response_type), response.status_code
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None, 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, 0


fetcher = AsyncHTTPFetcher()

        
# Ejemplo de uso
async def main():
    fetcher = AsyncHTTPFetcher()
    print(fetcher)
    another_fetcher = AsyncHTTPFetcher()
    print(another_fetcher)
    #content = await fetcher.fetch(url)
    #print(content)
    await AsyncHTTPFetcher.close_client()


if __name__ == "__main__":
    # Ejecutar el ejemplo
    import asyncio
    asyncio.run(main())