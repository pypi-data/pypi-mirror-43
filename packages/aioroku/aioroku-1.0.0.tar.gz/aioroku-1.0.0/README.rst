aioroku
=======

Screw remotes. Control your `Roku <http://www.roku.com>`_ via Python. Asynchronously.


Installation
------------

::

    pip install aioroku


Usage
-----


Requires Python 3.5 and uses asyncio and aiohttp.

::

    import asyncio
    import aiohttp
    from aioroku import AioRoku

   def get_args():
       arg_parser = ArgumentParser()
       arg_parser.add_argument('--roku_ip', '-r', metavar="ROKU_IP_ADDRESS")
       args = arg_parser.parse_args()
       return args.roku_ip

    async def main():
        async with aiohttp.ClientSession() as session:
            my_roku = AioRoku(host, session)
            print(await my_roku.active_app)
    
    if __name__ == '__main__':
        roku_ip = get_args()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(roku_ip))
        loop.close()



TODO
----

* Docs
* Tests, of course.
