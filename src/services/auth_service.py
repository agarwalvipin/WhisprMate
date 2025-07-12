"""Authentication service implementation."""

import streamlit as st

from ..core.models import AuthenticationInterface


class AuthenticationService(AuthenticationInterface):
    """Service for handling user authentication."""

    def __init__(
        self,
        enable_auth: bool = False,
        default_username: str = "admin",
        default_password: str = "admin"
    ):
        """Initialize authentication service.

        Args:
            enable_auth: Whether authentication is enabled
            default_username: Default username for authentication
            default_password: Default password for authentication
        """
        self.enable_auth = enable_auth
        self.default_username = default_username
        self.default_password = default_password

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
            username: Username
            password: Password

        Returns:
            True if login successful
        """
        # Simple demo authentication - in production, use proper auth
        if not self.enable_auth:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username or "user"
            return True

        # Check against default credentials
        if username == self.default_username and password == self.default_password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            return True

        return False

    def logout(self) -> None:
        """Log out user."""
        st.session_state["authenticated"] = False
        if "username" in st.session_state:
            del st.session_state["username"]

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
