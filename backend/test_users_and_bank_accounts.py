"""
Simple test script for User and BankAccount API
Run this after starting the server: uvicorn app.main:app --reload
"""
import requests

BASE_URL = "http://localhost:8000"

def test_users_and_bank_accounts():
    print("Testing User and BankAccount API...\n")
    
    try:
        # Test health endpoint first
        print("0. Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server. Is it running?")
        print("   Start with: cd backend && uvicorn app.main:app --reload")
        return
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Step 1: Create a User
    print("1. Creating a test user...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/users/", json=user_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            user = response.json()
            user_id = user["id"]
            print(f"   ✅ User created: {user}")
        else:
            print(f"   Response: {response.json()}")
            # Try to get existing user
            response = requests.get(f"{BASE_URL}/api/users/")
            users = response.json()
            if users:
                user_id = users[0]["id"]
                print(f"   Using existing user with ID: {user_id}")
            else:
                print("   ❌ No users found. Cannot continue.")
                return
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Step 2: Test GET /api/users/
    print("\n2. Testing GET /api/users/")
    try:
        response = requests.get(f"{BASE_URL}/api/users/")
        print(f"   Status: {response.status_code}")
        print(f"   Users: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 3: Test GET /api/bank-accounts/
    print("\n3. Testing GET /api/bank-accounts/")
    try:
        response = requests.get(f"{BASE_URL}/api/bank-accounts/")
        print(f"   Status: {response.status_code}")
        print(f"   Bank accounts: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 4: Create a BankAccount
    print(f"\n4. Creating a bank account for user {user_id}...")
    account_data = {
        "name": "My Checking Account",
        "currency": "USD",
        "initial_balance": 1000.0,
        "current_balance": 1000.0,
        "owner_id": user_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/bank-accounts/", json=account_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            account = response.json()
            account_id = account["id"]
            print(f"   ✅ Bank account created: {account}")
        else:
            print(f"   Response: {response.json()}")
            return
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Step 5: Test GET /api/bank-accounts/{account_id}
    print(f"\n5. Testing GET /api/bank-accounts/{account_id}")
    try:
        response = requests.get(f"{BASE_URL}/api/bank-accounts/{account_id}")
        print(f"   Status: {response.status_code}")
        print(f"   Bank account: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 6: Test UPDATE /api/bank-accounts/{account_id}
    print(f"\n6. Testing UPDATE /api/bank-accounts/{account_id}")
    update_data = {
        "current_balance": 1500.0
    }
    try:
        response = requests.put(f"{BASE_URL}/api/bank-accounts/{account_id}", json=update_data)
        print(f"   Status: {response.status_code}")
        print(f"   Updated bank account: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_users_and_bank_accounts()

