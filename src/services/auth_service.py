"""Authentication service implementation."""

import streamlit as st

from ..core.models import AuthenticationInterface


class AuthenticationService(AuthenticationInterface):
    """Service for handling user authentication."""

    def __init__(self, enable_auth: bool = False):
        """Initialize authentication service.

        Args:
            enable_auth: Whether authentication is enabled
        """
        self.enable_auth = enable_auth

    def is_authenticated(self) -> bool:
        """Check if user is authenticated.

        Returns:
            True if user is authenticated or auth is disabled
        """
        if not self.enable_auth:
            return True

        return st.session_state.get("authenticated", False)

    def login(self, username: str, password: str) -> bool:
        """Authenticate user.

        Args:
            username: Username (currently unused)
            password: Password (currently unused)

        Returns:
            True if login successful
        """
        # Simple demo authentication - in production, use proper auth
        if not self.enable_auth:
            st.session_state["authenticated"] = True
            return True

        # Demo: accept any non-empty credentials
        if username and password:
            st.session_state["authenticated"] = True
            return True

        return False

    def logout(self) -> None:
        """Log out user."""
        st.session_state["authenticated"] = False

    def require_auth(self) -> bool:
        """Check if authentication is required and user is authenticated.

        Returns:
            True if user can proceed, False if auth is required
        """
        if not self.enable_auth:
            return True

        return self.is_authenticated()

    def get_current_user(self) -> str:
        """Get current authenticated user.

        Returns:
            Username or 'Anonymous' if not authenticated
        """
        if self.is_authenticated():
            return st.session_state.get("username", "user")
        return "Anonymous"
