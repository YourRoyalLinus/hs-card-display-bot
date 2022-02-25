import unittest
import warnings

from random import randint
from aiohttp import ClientSession
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application, Response
from hearthstone import *
from hearthstone._parser import parse_api_result
from hearthstone.hearthstone import _make_request

class TestEndpoints(AioHTTPTestCase):
    
    async def setUpAsync(self) -> None:
        #Hide ResourceWarnings in JSONDecoder that occur during unittests
        #Assuming this is a non-functional issue that came about from changes 
        #to warnings in PY3.6: https://docs.python.org/3/whatsnew/3.6.html
        warnings.simplefilter("ignore", ResourceWarning)
        return await super().setUpAsync()

    async def tearDownAsync(self) -> None:
        warnings.simplefilter("default", ResourceWarning)
        return await super().tearDownAsync()

    async def get_application(self) -> Application:
        return Application()

    async def test_info_endpoint(self):
        res = await fetch_info(self.client.session)
        self.assertTrue(res)

    async def test_fetch_cards_endpoint(self):
        card = "Tunnel Trogg"
        res = await fetch_cards(self.client.session, card)
        self.assertTrue(res)

    async def test_fetch_cards_by_class_endpoint(self):
        class_ = "Mage"
        res = await fetch_cards_by_class(self.client.session, class_)

        self.assertTrue(res)

    async def test_fetch_cards_by_race_endpoint(self):
        race = "Mech"
        res = await fetch_cards_by_race(self.client.session, race)
        self.assertTrue(res)

    async def test_fetch_card_set_endpoint(self):
        set_ = "Knights of the Frozen Throne"
        res = await fetch_card_set(self.client.session, set_)
        self.assertTrue(res)

    async def test_fetch_cards_by_quality_endpoint(self):
        quality = "Rare"
        res = await fetch_cards_by_quality(self.client.session, quality)
        self.assertTrue(res)
    
    @unittest.skip("Cardbacks not implemented yet")
    async def test_fetch_cardbacks_endpoint(self):
        res = await fetch_cardbacks(self.client.session)
        self.assertTrue(res)
    
    async def test_fetch_card_by_partial_name_endpoint(self):
        partial_name = "Reno"
        res = await fetch_card_by_partial_name(self.client.session, 
                                                partial_name)
        self.assertTrue(res)
    
    async def test_fetch_cards_by_faction_endpoint(self):
        faction = "Horde"
        res = await fetch_cards_by_faction(self.client.session, faction)
        self.assertTrue(res)
    
    async def test_fetch_cards_by_type_endpoint(self):
        card_type = "Spell"
        res = await fetch_cards_by_type(self.client.session, card_type)
        self.assertTrue(res)
        
    async def test_fetch_all_cards_endpoint(self):
        res = await fetch_all_cards(self.client.session)
        self.assertTrue(res)

class TestAPIExceptions(AioHTTPTestCase):
    async def _card_not_found(*args):
        return Response(status=404, body=None, 
                        headers={"content-type": 'application/json'})

    async def _server_error(*args):
        server_error_code = randint(500, 599)
        return Response(status=server_error_code, body=None, 
                        headers={"content-type": 'application/json'})

    async def _http_exception(*args):
        general_error_code = randint(400, 599)
        return Response(status=general_error_code, body=None, 
                        headers={"content-type": 'application/json'})

    async def get_application(self):
        app = Application()

        app.router.add_get('/404', self._card_not_found)
        app.router.add_get('/500+', self._server_error)
        app.router.add_get('/*', self._http_exception)

        return app

    async def test_NoCardFound_exception_raised(self):
        with self.assertRaises(NoCardFound):
            url_ = "http://127.0.0.1:{}/404".format(self.client.port)
            await _make_request(self.client.session, url_, None, None)

    async def test_APIServerError_exception_raised(self):
        with self.assertRaises(APIServerError):
            url_ = "http://127.0.0.1:{}/500+".format(self.client.port)
            await _make_request(self.client.session, url_, None, None)

    async def test_HTTPException_exception_raised(self):
        with self.assertRaises(HTTPException):
            url_ = "http://127.0.0.1:{}/*".format(self.client.port)
            await _make_request(self.client.session, url_, None, None)

class TestAPIFunctionCalls(AioHTTPTestCase):
    _api_funcs = [fetch_cards, fetch_cards_by_class, fetch_cards_by_race, 
                    fetch_card_set, fetch_cards_by_quality, 
                    fetch_card_by_partial_name, fetch_cards_by_faction,
                    fetch_cards_by_type]

    async def get_application(self) -> Application:
        return Application()

    async def test_function_throws_exception(self):
        for api_callable in self._api_funcs:
            with self.subTest():
                with self.assertRaises(InvalidArgument):
                    await api_callable(self.client.session, "")

class TestParsing(unittest.TestCase):
        _card_data = [
            {"cardId": "0", "collectible": 1, 
            "name": "CollectibleCard"}, 
            {"cardId": "0", "name": "NonCollectibleCard"}
        ]

        def test_returns_multiple_cards(self):
            res = parse_api_result(self._card_data)
            self.assertIsInstance(res, MultipleCards)

        def test_returns_collectible_card(self):
            res = parse_api_result([self._card_data[0]])
            self.assertIsInstance(res, CollectibleCard)

        def test_returns_noncollectible_card(self):
            res = parse_api_result([self._card_data[1]])
            self.assertIsInstance(res, NonCollectibleCard)

API_TEST_SUITE = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestEndpoints),
    unittest.TestLoader().loadTestsFromTestCase(TestAPIExceptions),
    unittest.TestLoader().loadTestsFromTestCase(TestAPIFunctionCalls),
    unittest.TestLoader().loadTestsFromTestCase(TestParsing)
])


if __name__ == "__main__":
    unittest.main()