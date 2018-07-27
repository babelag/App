from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                author_request = client.post('/auth',
                                             data = json.dumps({'username' : 'test', 'password' : '1234'}),
                                             headers = {'Content-Type' : 'application/json'})
                self.auth_header = "JWT {}".format(json.loads(author_request.data)['access_token'])

    def test_get_item_no_auth(self):
        with self.app() as client:
                response = client.get('/item/test')

                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers = {'Authorization' : self.auth_header})
                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 11.99, 1).save_to_db()
                response = client.get('/item/test', headers = {'Authorization' : self.auth_header})
                self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 11.99, 1).save_to_db()

                response = client.delete('/item/test')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message' : 'Item deleted'}, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                response = client.post('/item/test', data = {'price' : 11.99, 'store_id' : 1})
                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name' : 'test', 'price' : 11.99}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 11.99, 1).save_to_db()
                response = client.post('/item/test', data={'price': 11.99, 'store_id': 1})
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test\' already exists.'}, json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.put('/item/test', data = {'price' : 11.99, 'store_id' : 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 11.99)
                self.assertDictEqual({'name' : 'test', 'price' : 11.99}, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 5.99)

                response = client.put('/item/test', data={'price': 11.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 11.99)
                self.assertDictEqual({'name': 'test', 'price': 11.99}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 11.99, 1).save_to_db()

                response = client.get('/items')

                self.assertEqual({'items' : [{'name' : 'test', 'price' : 11.99}]}, json.loads(response.data))