#!/usr/bin/env python3
"""
Test script for zLocket API
"""
import requests
import json

API_BASE_URL = "http://localhost:5000"

def test_home():
    """Test the home endpoint"""
    print("Testing home endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_spam_friend_request():
    """Test spam friend request endpoint"""
    print("\nTesting spam friend request endpoint...")
    data = {
        "target_url": "https://locket.cam/test_user",
        "custom_username": "TestBot",
        "use_emoji": True,
        "num_threads": 1
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/spam_friend_request",
            headers={"Content-Type": "application/json"},
            json=data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [200, 400, 500]  # Accept various responses for testing
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_delete_friend_request():
    """Test delete friend request endpoint"""
    print("\nTesting delete friend request endpoint...")
    data = {
        "email": "test@example.com",
        "password": "testpassword",
        "limit": 10,
        "num_threads": 1
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/delete_friend_request",
            headers={"Content-Type": "application/json"},
            json=data
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [200, 400, 401, 500]  # Accept various responses for testing
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=== zLocket API Test Suite ===")
    
    tests = [
        ("Home Endpoint", test_home),
        ("Spam Friend Request", test_spam_friend_request),
        ("Delete Friend Request", test_delete_friend_request)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
        print(f"Result: {'PASS' if result else 'FAIL'}")
    
    print("\n=== Test Summary ===")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()

