import asyncio
import httpx

from googletrans import Translator
from httpx_curl_cffi import AsyncCurlTransport


async def main():
    print("Creating googletrans Translator...")

    # googletrans creates its normal httpx.AsyncClient here.
    translator = Translator(
        service_urls=["translate.googleapis.com"],
        raise_exception=True,
    )

    # Keep a reference to the original client so we can close it properly.
    original_client = translator.client

    try:
        # Replace googletrans' HTTPX transport with curl-cffi.
        transport = AsyncCurlTransport(
            impersonate="chrome",
            default_headers=True,
        )

        translator.client = httpx.AsyncClient(
            transport=transport,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0.0.0 Safari/537.36"
                ),
            },
        )

        # googletrans' TokenAcquirer was created with the original
        # client, so point it at the replacement client as well.
        translator.token_acquirer.client = translator.client

        print("Testing translation...")
        print()

        result = await translator.translate(
            "Hello world",
            src="en",
            dest="de",
        )

        print("origin:", result.origin)
        print("text:  ", result.text)
        print("src:   ", result.src)
        print("dest:  ", result.dest)
        print("HTTP:  ", result._response.http_version)
        print("status:", result._response.status_code)

    except Exception as e:
        print()
        print("ERROR:")
        print(type(e).__name__, e)

    finally:
        await translator.client.aclose()
        await original_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())