from aioroku import AioRoku, Application
import asyncio

import aiohttp

TO = aiohttp.ClientTimeout(total=5)


async def main():
    hue_host = 'HUE_HUB_IPADDRESS'
    async with aiohttp.ClientSession(timeout=TO) as session:
        fauxku = AioRoku(hue_host, session)
        foo = await fauxku.device_info
        print(foo)
        print(fauxku.sw_info)
        print(await fauxku.apps)
        print(await fauxku.power_state)
        print(await fauxku.active_app)
        print(await fauxku.apps)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
