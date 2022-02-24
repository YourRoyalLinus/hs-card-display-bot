import unittest
from random import randint
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application, Response

from hearthstone import *
from hearthstone._parser import parse_api_result
from hearthstone.hearthstone import _make_request

#TODO
#Break into test_api.py and test_card_obj.py
#rewrite/organize the classes and methods in each test module
 #is testing private methods too bad practice here (TEST BY CALLING A fetch_cards AND MOCKING THE SERVER!!!)
#non-functional testing

class TestEndpoints(AioHTTPTestCase): 
    async def get_application(self) -> Application:
        return Application()

    async def test_info_endpoint(self):
        res = await fetch_info(self.client.session)
        self.assertTrue(res)

    async def test_fetch_cards_endpoint(self):
        _card = "Tunnel Trogg"
        res = await fetch_cards(self.client.session, _card)
        self.assertTrue(res)

    async def test_fetch_cards_by_class_endpoint(self):
        _class = "Mage"
        res = await fetch_cards_by_class(self.client.session, _class)
        self.assertTrue(res)

    async def test_fetch_cards_by_race_endpoint(self):
        _race = "Mech"
        res = await fetch_cards_by_race(self.client.session, _race)
        self.assertTrue(res)

    async def test_fetch_card_set_endpoint(self):
        _set = "Knights of the Frozen Throne"
        res = await fetch_card_set(self.client.session, _set)
        self.assertTrue(res)

    async def test_fetch_cards_by_quality_endpoint(self):
        _quality = "Rare"
        res = await fetch_cards_by_quality(self.client.session, _quality)
        self.assertTrue(res)
    
    @unittest.skip("Cardbacks not implemented yet")
    async def test_fetch_cardbacks_endpoint(self):
        res = await fetch_cardbacks(self.client.session)
        self.assertTrue(res)
    
    async def test_fetch_card_by_partial_name_endpoint(self):
        _partial_name = "Reno"
        res = await fetch_card_by_partial_name(self.client.session, _partial_name)
        self.assertTrue(res)
    
    async def test_fetch_cards_by_faction_endpoint(self):
        _faction = "Horde"
        res = await fetch_cards_by_faction(self.client.session, _faction)
        self.assertTrue(res)
    
    async def test_fetch_cards_by_type_endpoint(self):
        _card_type = "Spell"
        res = await fetch_cards_by_type(self.client.session, _card_type)
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
            _url = "http://127.0.0.1:{}/404".format(self.client.port)
            fetch_cards.__dict__["endpoint"] = _url
            await fetch_cards(self.client.session, "card_name")
            #await _make_request(self.client.session, _url, None, None)

    async def test_APIServerError_exception_raised(self):
        with self.assertRaises(APIServerError):
            _url = "http://127.0.0.1:{}/500+".format(self.client.port)
            await _make_request(self.client.session, _url, None, None)

    async def test_HTTPException_exception_raised(self):
        _url = "http://127.0.0.1:{}/*".format(self.client.port)
        with self.assertRaises(HTTPException):
            await _make_request(self.client.session, _url, None, None)

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

class TestCard(unittest.TestCase):
    _multipleCards = MultipleCards([
                {"cardId": "0", "collectible": 1, "name": "CollectibleCard"}, 
                {"cardId": "1", "name": "NonCollectibleCard"}
            ])

    def test_is_card_invalid(self):
        _card = CollectibleCard({})

        self.assertEqual("Invalid Card", str(_card))
    
    def test_is_card(self):
        _card_false = CollectibleCard({"Name": "Test", "Empty": None})
        _card_true = CollectibleCard({"Name": "Test", "Empty": True})

        self.assertFalse(_card_false)
        self.assertTrue(_card_true)

    def test_card_equality(self):
        _card_one = CollectibleCard({"cardId": "0", "collectible": 1})
        _card_one_clone = CollectibleCard({"cardId": "0", "collectible": 1})
        _card_two =CollectibleCard({"cardId": "1", "collectible": 1})

        self.assertEqual(_card_one, _card_one_clone)
        self.assertNotEqual(_card_one, _card_two)

    def test_multiplecards_return_card_object(self):
        _card_by_name = self._multipleCards["CollectibleCard"]
        _card_by_ix = CollectibleCard(self._multipleCards[0])

        self.assertEqual(_card_by_name, _card_by_ix)
    
    def test_multiplecards_throws_NoCardFound(self):
        with self.assertRaises(NoCardFound):
            self._multipleCards["NA"]

    def test_multiplecards_equality(self):
        _multiple_cards_clone = MultipleCards([
                {"cardId": "0", "collectible": 1, "name": "CollectibleCard"}, 
                {"cardId": "1", "name": "NonCollectibleCard"}
            ])
    
        self.assertEqual(self._multipleCards, _multiple_cards_clone)

        _multiple_cards_two = _multiple_cards_clone._cards.append(
                                             {"cardId": "0", "collectible": 1})

        self.assertNotEqual(self._multipleCards, _multiple_cards_two)

def run_all_test_suites():
    test_classes_to_run = [TestEndpoints, TestAPIExceptions,
                           TestAPIFunctionCalls, TestParsing,
                           TestCard]
    
    loader = unittest.TestLoader()
    suites_list = [loader.loadTestsFromTestCase(test) 
                    for test in test_classes_to_run]

    main_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()

    results = runner.run(main_suite)

if __name__ == "__main__":
    run_all_test_suites()