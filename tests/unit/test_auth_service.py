#!/usr/bin/env python3
"""
Unit tests for the authentication service.
This module tests the AuthenticationService class independently.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.auth_service import AuthenticationService


def test_authentication():
    """Test the authentication service."""
    print("Testing Authentication Service...")
    
    # Test with default credentials
    auth_service = AuthenticationService(
        enable_auth=True,
        default_username="testuser",
        default_password="testpass"
    )
    
    print(f"Default username: {auth_service.default_username}")
    print(f"Default password: {auth_service.default_password}")
    print(f"Authentication enabled: {auth_service.enable_auth}")
    
    # Mock session state for testing (since we're not in Streamlit)
    class MockSessionState:
        def __init__(self):
            self.data = {}
        
        def get(self, key, default=None):
            return self.data.get(key, default)
        
        def __setitem__(self, key, value):
            self.data[key] = value
        
        def __contains__(self, key):
            return key in self.data
        
        def __delitem__(self, key):
            if key in self.data:
                del self.data[key]
    
    # Mock streamlit session state
    import streamlit as st
    st.session_state = MockSessionState()
    
    # Test authentication
    print("\n--- Testing Authentication ---")
    
    # Test with correct credentials
    print("Testing with correct credentials...")
    result = auth_service.login("testuser", "testpass")
    print(f"Login result: {result}")
    print(f"Is authenticated: {auth_service.is_authenticated()}")
    print(f"Current user: {auth_service.get_current_user()}")
    
    # Test logout
    print("\nTesting logout...")
    auth_service.logout()
    print(f"Is authenticated after logout: {auth_service.is_authenticated()}")
    
    # Test with incorrect credentials
    print("\nTesting with incorrect credentials...")
    result = auth_service.login("wronguser", "wrongpass")
    print(f"Login result: {result}")
    print(f"Is authenticated: {auth_service.is_authenticated()}")
    
    # Test with disabled authentication
    print("\n--- Testing Disabled Authentication ---")
    auth_service_disabled = AuthenticationService(enable_auth=False)
    result = auth_service_disabled.login("any", "credentials")
    print(f"Login result (auth disabled): {result}")
    print(f"Is authenticated (auth disabled): {auth_service_disabled.is_authenticated()}")
    
    print("\n✅ Authentication tests completed!")


if __name__ == "__main__":
    test_authentication()
