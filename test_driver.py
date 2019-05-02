import unittest
import os
import json
from my_app import create_app, db


class FindDriverTestCase(unittest.TestCase):

    def setup(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.driver_info = {'loc': 1.345000, 'lat': 1.345000, 'acc': 0.8}

        with self.app.app_context():
            db.create_all()

    def test_location_creation(self):
        """Test API can create a location from driver (POST request)"""
        res = self.client().post('/locations/', data=self.driver_info)
        self.assertEqual(res.status_code, 201)
        self.assertIn('0.8', str(res.data))

    def test_location_update(self):
        """
        Test API can update driver's location (PUT Request)
        """
        res = self.client().post(
            '/locations/', data={'loc': 1.345000, 'lat': 1.345000, 'acc': 0.8})
        self.assertEqual(res.status_code, 201)

        result_in_json = json.loads(res.data.decode('utf-8').replace("'","\""))
        driver_id=result_in_json['id']

        res=self.client().put('/drivers/{}/location'.format(driver_id),
                        data={'loc': 1.345001, 'lat': 1.345001, 'acc': 0.5})
        self.assertEqual(res.status_code, 200)
        results=self.client().get('/bucketlists/1')
        self.assertIn('1.345001', str(results.data))

    def tear_down(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
