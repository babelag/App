from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')

                self.assertEqual(response.status_code, 401)


    def test_get_item_not_found(self):
        pass

    def test_get_item(self):
        pass

    def test_delete_item(self):
        pass

    def test_create_item(self):
        pass

    def test_create_duplicate_item(self):
        pass

    def test_put_item(self):
        pass

    def test_put_update_item(self):
        pass

    def test_item_list(self):
        pass