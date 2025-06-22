#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime, timedelta
import unittest
import sys
import os
from dotenv import load_dotenv

# Load environment variables from frontend/.env to get the backend URL
load_dotenv('/app/frontend/.env')

# Get the backend URL from environment variables
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL')
if not BACKEND_URL:
    print("Error: REACT_APP_BACKEND_URL not found in environment variables")
    sys.exit(1)

# Admin credentials
ADMIN_PASSWORD = "Rbcadminpass2025"

# Test data for creating a giveaway
def create_test_giveaway_data():
    # Create a giveaway that ends 7 days from now
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    return {
        "title": "Test Giveaway",
        "description": "This is a test giveaway created by the automated test script",
        "prize": "Test Prize",
        "endDate": end_date,
        "entryRequirement": "Join our Discord server"
    }

class RBCCommunityAPITest(unittest.TestCase):
    def setUp(self):
        self.base_url = BACKEND_URL
        self.api_url = f"{BACKEND_URL}/api"
        self.created_giveaway_id = None
        print(f"\nUsing backend URL: {self.base_url}")

    def tearDown(self):
        # Clean up any created giveaways
        if self.created_giveaway_id:
            try:
                self._delete_giveaway(self.created_giveaway_id)
                print(f"Cleaned up test giveaway with ID: {self.created_giveaway_id}")
            except Exception as e:
                print(f"Warning: Failed to clean up test giveaway: {e}")

    def _delete_giveaway(self, giveaway_id):
        """Helper method to delete a giveaway"""
        response = requests.delete(f"{self.api_url}/admin/giveaways/{giveaway_id}")
        return response

    def test_01_root_endpoint(self):
        """Test the root endpoint"""
        print("\n--- Testing Root Endpoint ---")
        response = requests.get(self.base_url)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("RBC Community API is running", data["message"])

    def test_02_health_check(self):
        """Test the health check endpoint"""
        print("\n--- Testing Health Check Endpoint ---")
        response = requests.get(f"{self.api_url}/health")
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "healthy")
        self.assertIn("database", data)
        self.assertEqual(data["database"], "connected")

    def test_03_get_giveaways(self):
        """Test fetching all giveaways"""
        print("\n--- Testing Get All Giveaways Endpoint ---")
        response = requests.get(f"{self.api_url}/giveaways")
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text[:200]}...")  # Truncate long responses
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        
        # Print the number of giveaways found
        print(f"Found {len(data)} giveaways")

    def test_04_get_active_giveaways(self):
        """Test fetching active giveaways"""
        print("\n--- Testing Get Active Giveaways Endpoint ---")
        response = requests.get(f"{self.api_url}/giveaways/active")
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text[:200]}...")  # Truncate long responses
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        
        # Print the number of active giveaways found
        print(f"Found {len(data)} active giveaways")

    def test_05_get_community_stats(self):
        """Test fetching community statistics"""
        print("\n--- Testing Community Stats Endpoint ---")
        response = requests.get(f"{self.api_url}/stats")
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("totalGiveaways", data)
        self.assertIn("activeGiveaways", data)
        self.assertIn("memberCount", data)
        self.assertIn("communityStatus", data)

    def test_06_admin_login_success(self):
        """Test admin login with correct password"""
        print("\n--- Testing Admin Login (Success) ---")
        payload = {"password": ADMIN_PASSWORD}
        response = requests.post(f"{self.api_url}/admin/login", json=payload)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("Admin authenticated successfully", data["message"])
        self.assertEqual(data["status"], "success")

    def test_07_admin_login_failure(self):
        """Test admin login with incorrect password"""
        print("\n--- Testing Admin Login (Failure) ---")
        payload = {"password": "wrong_password"}
        response = requests.post(f"{self.api_url}/admin/login", json=payload)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Invalid admin password", data["detail"])

    def test_08_create_giveaway(self):
        """Test creating a new giveaway"""
        print("\n--- Testing Create Giveaway ---")
        giveaway_data = create_test_giveaway_data()
        print(f"Creating giveaway with data: {json.dumps(giveaway_data, indent=2)}")
        
        response = requests.post(f"{self.api_url}/admin/giveaways", json=giveaway_data)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], giveaway_data["title"])
        self.assertEqual(data["description"], giveaway_data["description"])
        self.assertEqual(data["prize"], giveaway_data["prize"])
        
        # Store the created giveaway ID for later tests and cleanup
        self.created_giveaway_id = data["id"]
        print(f"Created giveaway with ID: {self.created_giveaway_id}")

    def test_09_create_giveaway_past_date(self):
        """Test creating a giveaway with a past end date (should fail)"""
        print("\n--- Testing Create Giveaway with Past Date (Should Fail) ---")
        # Create a giveaway that ended yesterday
        past_date = (datetime.now() - timedelta(days=1)).isoformat()
        giveaway_data = {
            "title": "Past Test Giveaway",
            "description": "This giveaway has already ended",
            "prize": "Nothing",
            "endDate": past_date,
            "entryRequirement": "Join our Discord server"
        }
        
        print(f"Creating giveaway with past date: {json.dumps(giveaway_data, indent=2)}")
        response = requests.post(f"{self.api_url}/admin/giveaways", json=giveaway_data)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("End date must be in the future", data["detail"])

    def test_10_create_giveaway_invalid_date(self):
        """Test creating a giveaway with an invalid date format (should fail)"""
        print("\n--- Testing Create Giveaway with Invalid Date (Should Fail) ---")
        giveaway_data = {
            "title": "Invalid Date Giveaway",
            "description": "This giveaway has an invalid date",
            "prize": "Nothing",
            "endDate": "not-a-date",
            "entryRequirement": "Join our Discord server"
        }
        
        print(f"Creating giveaway with invalid date: {json.dumps(giveaway_data, indent=2)}")
        response = requests.post(f"{self.api_url}/admin/giveaways", json=giveaway_data)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Invalid date format", data["detail"])

    def test_11_update_giveaway(self):
        """Test updating a giveaway"""
        # First create a giveaway to update
        if not self.created_giveaway_id:
            self.test_08_create_giveaway()
            
        print("\n--- Testing Update Giveaway ---")
        giveaway_id = self.created_giveaway_id
        updated_data = {
            "title": "Updated Test Giveaway",
            "description": "This giveaway has been updated",
            "prize": "Updated Prize",
            "endDate": (datetime.now() + timedelta(days=14)).isoformat(),
            "entryRequirement": "Updated requirement"
        }
        
        print(f"Updating giveaway {giveaway_id} with data: {json.dumps(updated_data, indent=2)}")
        response = requests.put(f"{self.api_url}/admin/giveaways/{giveaway_id}", json=updated_data)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], giveaway_id)
        self.assertEqual(data["title"], updated_data["title"])
        self.assertEqual(data["description"], updated_data["description"])
        self.assertEqual(data["prize"], updated_data["prize"])

    def test_12_delete_giveaway(self):
        """Test deleting a giveaway"""
        # First create a giveaway to delete if we don't have one
        if not self.created_giveaway_id:
            self.test_08_create_giveaway()
            
        print("\n--- Testing Delete Giveaway ---")
        giveaway_id = self.created_giveaway_id
        
        print(f"Deleting giveaway with ID: {giveaway_id}")
        response = self._delete_giveaway(giveaway_id)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("Giveaway deleted successfully", data["message"])
        
        # Verify the giveaway is gone by trying to fetch it
        print("Verifying giveaway was deleted...")
        response = requests.get(f"{self.api_url}/giveaways")
        all_giveaways = response.json()
        giveaway_ids = [g["id"] for g in all_giveaways]
        self.assertNotIn(giveaway_id, giveaway_ids)
        
        # Clear the ID since we've deleted it
        self.created_giveaway_id = None

    def test_13_delete_nonexistent_giveaway(self):
        """Test deleting a giveaway that doesn't exist"""
        print("\n--- Testing Delete Nonexistent Giveaway ---")
        fake_id = "nonexistent-id-12345"
        
        print(f"Attempting to delete nonexistent giveaway with ID: {fake_id}")
        response = self._delete_giveaway(fake_id)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("Giveaway not found", data["detail"])

if __name__ == "__main__":
    print(f"Starting RBC Community API Tests against {BACKEND_URL}")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)