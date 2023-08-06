from aioroku.core import AioRoku

from aiohttp import ClientSession, ClientTimeout
from asynctest import patch, CoroutineMock

TO = ClientTimeout(total=5)


@patch('aiohttp.ClientSession._request')
async def test_power_state(mock_req):
    """Ensures returns the power state from power-mode node of device-info."""
    mock_req.return_value.read = CoroutineMock()
    mock_req.return_value.read.return_value = '''<?xml version="1.0" encoding=
    "UTF-8" ?><device-info><power-mode>Headless</power-mode></device-info>'''
    async with ClientSession(timeout=TO) as sesh:
        fauxku = AioRoku('6.6.6', session=sesh)
        power = await fauxku.power_state
        assert power == 'Headless'
    assert mock_req.assert_awaited


@patch('aiohttp.ClientSession._request')
async def test_active_app(mock_req):
    """Tests the correct app is returned on three calls to active_app method. """
    mock_req.return_value.read = CoroutineMock()
    mock_req.return_value.read.side_effect = ['''<?xml version="1.0" encoding=
    "UTF-8" ?>
    <active-app>
    <app id="12" subtype="ndka" type="appl" version="4.2.81179021">Netflix</app>
    </active-app>''', '''<?xml version="1.0" encoding="UTF-8" ?>
    <active-app>
    <app>Roku</app>
    <screensaver id="72728" subtype="sdka" type="ssvr"
    version="2.3.47">Photo Collage</screensaver>
    </active-app>''', '''<?xml version="1.0" encoding="UTF-8" ?>
    <active-app>
    <app>Roku</app>
    </active-app>''']
    async with ClientSession(timeout=TO) as sesh:
        fauxku = AioRoku('6.6.6', session=sesh)
        app = await fauxku.active_app
        assert app.name == 'Netflix'
        next_app = await fauxku.active_app
        assert next_app.is_screensaver is True
        third_app = await fauxku.active_app
        assert third_app.name == 'Roku'
        assert mock_req.await_count == 3

