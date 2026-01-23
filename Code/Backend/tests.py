import unittest
import json
from app import create_app
from models import ParkingLot
from config import Config

class TestBackend(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and reset database before each test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Reset the Singleton instance to ensure a clean state for every test
        # This prevents "test_A" from affecting "test_B"
        ParkingLot._instance = None
        self.parking_lot = ParkingLot()

    def test_01_health_check(self):
        """Test if the API is running (Health Check)"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Smart Parking System API is running")

    def test_02_initial_status(self):
        """Test fetching initial parking status"""
        response = self.client.get('/api/parking/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Verify we have slots
        self.assertTrue(len(data['slots']) > 0)
        # Verify structure keys exist
        self.assertIn('available_count', data)
        self.assertIn('total_count', data)

    def test_03_successful_booking(self):
        """Test booking a valid empty slot"""
        payload = {
            'slot_id': 'A1',
            'vehicle_id': 'MH-01-AB-1234'
        }
        response = self.client.post('/api/parking/book', 
                                  data=json.dumps(payload),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['vehicle_id'], 'MH-01-AB-1234')

    def test_04_prevent_double_booking(self):
        """Test Reliability: Prevent booking an already occupied slot"""
        # Step 1: Book A1
        first_booking = {
            'slot_id': 'A1',
            'vehicle_id': 'MH-01-AB-1234'
        }
        self.client.post('/api/parking/book', 
                        data=json.dumps(first_booking),
                        content_type='application/json')
        
        # Step 2: Try to book A1 again (Double Booking)
        second_booking = {
            'slot_id': 'A1',
            'vehicle_id': 'KA-05-XY-9999'
        }
        response = self.client.post('/api/parking/book', 
                                  data=json.dumps(second_booking),
                                  content_type='application/json')
        
        # Expect Failure (409 Conflict)
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn("already occupied", data['message'])

    def test_05_release_slot(self):
        """Test releasing a booked slot"""
        # First book it
        self.client.post('/api/parking/book', 
                        data=json.dumps({'slot_id': 'B1', 'vehicle_id': 'MH-02-ZZ-1111'}),
                        content_type='application/json')
        
        # Then release it
        response = self.client.post('/api/parking/release', 
                                  data=json.dumps({'slot_id': 'B1'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_06_invalid_input(self):
        """Test Usability: System should handle missing data gracefully"""
        # Send empty JSON
        response = self.client.post('/api/parking/book', 
                                  data=json.dumps({}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_07_vehicle_id_constraint(self):
        """Test Reliability: Verify the Regex validation for Vehicle ID"""
        # This assumes you added the constraint verification we discussed!
        payload = {
            'slot_id': 'C1',
            'vehicle_id': '!!!INVALID!!!'
        }
        response = self.client.post('/api/parking/book', 
                                  data=json.dumps(payload),
                                  content_type='application/json')
        
        # If you added the regex, this should be 400. 
        # If you didn't add the regex, this test might fail (return 200).
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Invalid Vehicle ID", data['message'])

if __name__ == '__main__':
    unittest.main()
