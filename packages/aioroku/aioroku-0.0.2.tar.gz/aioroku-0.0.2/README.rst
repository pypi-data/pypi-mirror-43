python-roku
===========

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

    async def main():
        async with aiohttp.ClientSession() as session:
            await run(session)


    async def run(websession):



The Basics
~~~~~~~~~~



Apps
~~~~


Entering Text
~~~~~~~~~~~~~



Advanced Stuff
--------------


Discovery
~~~~~~~~~


Sensors
~~~~~~~


Touch
~~~~~


Generic Input
~~~~~~~~~~~~~


TODO
----

* Docs
* Tests, of course.
