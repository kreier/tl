import asyncio
from googletrans import Translator

async def main():
    async with Translator(
        service_urls=["translate.googleapis.com"]
    ) as translator:
        result = await translator.translate(
            "Hello world",
            src="en",
            dest="de",
        )

        print(result)
        print("HTTP:", result._response.http_version)
        print("status:", result._response.status_code)

asyncio.run(main())