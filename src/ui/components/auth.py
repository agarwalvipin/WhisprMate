"""Authentication UI components."""

import streamlit as st

from ...services.auth_service import AuthenticationService


class AuthComponent:
    """Component for handling authentication UI."""

    def __init__(self, auth_service: AuthenticationService):
        """Initialize auth component.

        Args:
            auth_service: Authentication service instance
        """
        self.auth_service = auth_service

    def render_sidebar_auth(self) -> bool:
        """Render authentication UI in sidebar.

        Returns:
            True if user is authenticated
        """
        if not self.auth_service.enable_auth:
            return True

        with st.sidebar:
            st.markdown("### 🔐 Authentication")

            if self.auth_service.is_authenticated():
                st.success(f"✅ Logged in as {self.auth_service.get_current_user()}")
                if st.button("🚪 Logout"):
                    self.auth_service.logout()
                    st.rerun()
                return True
            else:
                st.info("🔒 Please log in to continue.")

                with st.form("login_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    submitted = st.form_submit_button("🔑 Login")

                    if submitted:
                        if self.auth_service.login(username, password):
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")

                return False

    def render_login_page(self) -> bool:
        """Render full-page login interface.

        Returns:
            True if user is authenticated
        """
        if self.auth_service.is_authenticated():
            return True

        st.title("🔐 Login Required")
        st.markdown("Please log in to access the application.")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            with st.container():
                st.markdown(
                    """
                    <div style="
                        background: white;
                        padding: 2rem;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin: 2rem 0;
                    ">
                """,
                    unsafe_allow_html=True,
                )

                with st.form("main_login_form"):
                    st.markdown("#### Enter your credentials")
                    username = st.text_input("👤 Username", placeholder="Enter username")
                    password = st.text_input(
                        "🔒 Password", type="password", placeholder="Enter password"
                    )

                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        submitted = st.form_submit_button("🔑 Login", use_container_width=True)
                    with col_btn2:
                        guest = st.form_submit_button("👤 Guest Access", use_container_width=True)

                    if submitted:
                        if self.auth_service.login(username, password):
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please try again.")

                    elif guest:
                        # Allow guest access
                        self.auth_service.login("guest", "guest")
                        st.success("Logged in as guest!")
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

        return False

    def require_authentication(self) -> bool:
        """Ensure user is authenticated or show login.

        Returns:
            True if user can proceed
        """
        if not self.auth_service.enable_auth:
            return True

        if self.auth_service.is_authenticated():
            return True

        self.render_login_page()
        return False
