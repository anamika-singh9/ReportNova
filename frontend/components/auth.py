import streamlit as st

from frontend.api.backend import (
    login,
    signup,
    get_reports,
    get_current_user,
)

from frontend.services.session import (
    save_login,
    save_reports,
)


def render_auth_page():
    """
    Render Login and Signup page.
    """

    st.title("🤖 AI Research Lab")

    st.caption(
        "Login to generate and manage your AI research reports."
    )

    login_tab, signup_tab = st.tabs(
        ["Login", "Sign Up"]
    )

    # ==========================================
    # LOGIN
    # ==========================================

    with login_tab:

        with st.form("login_form"):

            email = st.text_input(
                "Email"
            )

            password = st.text_input(
                "Password",
                type="password",
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        if submitted:

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                try:

                    # ==================================
                    # LOGIN REQUEST
                    # ==================================

                    response = login(
                        email=email,
                        password=password,
                    )

                    access_token = response.get(
                        "access_token"
                    )

                    if not access_token:

                        st.error(
                            "Login failed. Access token not received."
                        )

                    else:

                        # ==================================
                        # GET CURRENT USER
                        # ==================================

                        user = get_current_user(
                            access_token=access_token,
                        )

                        # ==================================
                        # SAVE LOGIN SESSION
                        # ==================================

                        save_login(
                            access_token=access_token,
                            user=user,
                        )

                        # ==================================
                        # LOAD USER REPORTS
                        # ==================================

                        reports = get_reports(
                            access_token=access_token,
                        )

                        save_reports(
                            reports
                        )

                        st.success(
                            "Login successful!"
                        )

                        st.rerun()

                except Exception as e:

                    st.error(
                        str(e)
                    )

    # ==========================================
    # SIGNUP
    # ==========================================

    with signup_tab:

        with st.form("signup_form"):

            name = st.text_input(
                "Name"
            )

            email = st.text_input(
                "Email",
                key="signup_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password",
            )

            submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True,
            )

        if submitted:

            if not name or not email or not password:

                st.warning(
                    "Please fill all fields."
                )

            else:

                try:

                    signup(
                        name=name,
                        email=email,
                        password=password,
                    )

                    st.success(
                        "Account created successfully. "
                        "Please login."
                    )

                except Exception as e:

                    st.error(
                        str(e)
                    )