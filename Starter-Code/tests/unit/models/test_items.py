import unittest

from models.item import ItemModel

class ItemTest(unittest.TestCase):

    def test_create_item(self):
        item = ItemModel('test', 11.99)

        self.assertEqual(item.name, 'test',
                         "Test name of the item after creation does not equal the constructor argument")
        self.assertEqual(item.price, 11.99,
                         "Test price of the item after creation does not equal the constructor argument")

    def test_item_json(self):
        item = ItemModel('test', 11.99)
        expected = {
            'name' : 'test',
            'price' : 11.99
        }

        self.assertEqual(item.json(), expected,
                         "The JSON export of the item is incorrect. Received {}, expected {}"
                         .format(item.json(), expected))

