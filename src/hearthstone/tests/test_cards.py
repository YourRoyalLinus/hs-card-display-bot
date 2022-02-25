import unittest
from hearthstone._card import *
from hearthstone.errors import NoCardFound

class TestCard(unittest.TestCase):
    _multipleCards = MultipleCards([
                {"cardId": "0", "collectible": 1, "name": "CollectibleCard"}, 
                {"cardId": "1", "name": "NonCollectibleCard"}
    ])

    def test_is_card_invalid(self):
        card = CollectibleCard({})

        self.assertEqual("Invalid Card", str(card))
    
    def test_is_card(self):
        card_false = CollectibleCard({"Name": "Test", "Empty": None})
        card_true = CollectibleCard({"Name": "Test", "Empty": True})

        self.assertFalse(card_false)
        self.assertTrue(card_true)

    def test_card_equality(self):
        card_one = CollectibleCard({"cardId": "0", "collectible": 1})
        card_one_clone = CollectibleCard({"cardId": "0", "collectible": 1})
        card_two =CollectibleCard({"cardId": "1", "collectible": 1})

        self.assertEqual(card_one, card_one_clone)
        self.assertNotEqual(card_one, card_two)

    def test_multiplecards_return_card_object(self):
        card_by_name = self._multipleCards["CollectibleCard"]
        card_by_ix = CollectibleCard(self._multipleCards[0])

        self.assertEqual(card_by_name, card_by_ix)
    
    def test_multiplecards_throws_NoCardFound(self):
        with self.assertRaises(NoCardFound):
            self._multipleCards["NA"]

    def test_multiplecards_equality(self):
        multiple_cards_clone = MultipleCards([
                {"cardId": "0", "collectible": 1, "name": "CollectibleCard"}, 
                {"cardId": "1", "name": "NonCollectibleCard"}
        ])
    
        self.assertEqual(self._multipleCards, multiple_cards_clone)

        multiple_cards_two = multiple_cards_clone._cards.append(
                                             {"cardId": "0", "collectible": 1})

        self.assertNotEqual(self._multipleCards, multiple_cards_two)


CARD_TEST_SUITE = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestCard)
])

if __name__ == "__main__":
    unittest.main()