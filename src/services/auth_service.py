"""Authentication service implementation."""

import streamlit as st

from config.logging_config import get_logger

from ..core.models import AuthenticationInterface

logger = get_logger("auth")


class AuthenticationService(AuthenticationInterface):
    """Service for handling user authentication."""

    def __init__(
        self,
        enable_auth: bool = False,
        default_username: str = "admin",
        default_password: str = "admin",
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
        logger.info(f"AuthenticationService initialized: enabled={enable_auth}")
        logger.debug(f"Authentication settings: enable_auth={enable_auth}")

        # Initialize session state for authentication
        self._init_session_state()

    def _init_session_state(self) -> None:
        """Initialize authentication session state."""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        if "username" not in st.session_state:
            st.session_state.username = None
        if "session_id" not in st.session_state:
            import uuid

            st.session_state.session_id = str(uuid.uuid4())
            logger.debug(f"New session initialized: {st.session_state.session_id}")

    def is_authenticated(self) -> bool:
        """Check if user is authenticated.

        Returns:
            True if user is authenticated or auth is disabled
        """
        if not self.enable_auth:
            return True

        # Ensure session state is initialized
        self._init_session_state()

        # Check authentication status
        is_auth = st.session_state.get("authenticated", False)
        username = st.session_state.get("username")

        if is_auth and username:
            logger.debug(
                f"User {username} is authenticated (session: {st.session_state.get('session_id', 'unknown')})"
            )
            return True

        logger.debug("User is not authenticated")
        return False

    def login(self, username: str, password: str) -> bool:
        """Authenticate user.

        Args:
            username: Username
            password: Password

        Returns:
            True if login successful
        """
        logger.debug(f"Login attempt for username: {username}")

        # Ensure session state is initialized
        self._init_session_state()

        # Simple demo authentication - in production, use proper auth
        if not self.enable_auth:
            logger.info("Authentication disabled, auto-login")
            st.session_state["authenticated"] = True
            st.session_state["username"] = username or "user"
            return True

        # Check against default credentials
        if username == self.default_username and password == self.default_password:
            logger.info(f"Successful login for user: {username}")
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            return True

        logger.warning(f"Failed login attempt for username: {username}")
        return False

    def logout(self) -> None:
        """Log out user."""
        logger.info(f"User {st.session_state.get('username', 'unknown')} logging out")
        st.session_state["authenticated"] = False
        st.session_state["username"] = None

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
