import asyncio
import httpx

async def test_rate_limit():
    url = "http://127.0.0.1:8000/"
    async with httpx.AsyncClient() as client:
        # Fire off 5 requests quickly to test rate limiting
        tasks = [client.get(url) for _ in range(5)]
        responses = await asyncio.gather(*tasks)

        for i, r in enumerate(responses, start=1):
            print(f"Request {i}: {r.status_code} {r.text}")

if __name__ == "__main__":
    asyncio.run(test_rate_limit())