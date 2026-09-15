import os
import base64

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
    logo_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets",
            "reportnova_logo.png",  # replace this asset with the new transparent PNG
        )
    )

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as _logo_file:
            _logo_b64 = base64.b64encode(_logo_file.read()).decode()

        st.markdown(
            """
            <style>
            .reportnova-logo-wrap {
                display: flex;
                justify-content: center;
                align-items: center;
                background: transparent;
                margin: 0 auto 1rem auto;
                padding: 0;
            }
            .reportnova-logo-wrap img {
                width: 260px;
                max-width: 100%;
                height: auto;
                display: block;
                background: transparent;
                border: none;
                outline: none;
                box-shadow: none;
                border-radius: 0;
                mix-blend-mode: normal;
            }
            div[data-testid="stImage"] {
                background: transparent !important;
                box-shadow: none !important;
                border: none !important;
            }
            div[data-testid="stImage"] > img {
                background: transparent !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="reportnova-logo-wrap">
                <img src="data:image/png;base64,{_logo_b64}" alt="ReportNova logo" />
            </div>
            """,
            unsafe_allow_html=True,
        )

    login_tab, signup_tab = st.tabs(
        [
            "🔑 Login",
            "📝 Sign Up",
        ]
    )

    with login_tab:
        st.subheader("Welcome back")

        with st.form("login_form"):
            email = st.text_input(
                "Email",
                key="login_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )

            submitted = st.form_submit_button(
                "Login",
                width="stretch",
            )

        if submitted:
            if not email or not password:
                st.error(
                    "Please enter your email and password."
                )
            else:
                try:
                    response = login(
                        email=email,
                        password=password,
                    )

                    access_token = response.get(
                        "access_token"
                    )

                    if not access_token:
                        raise RuntimeError(
                            "Login failed. No access token received."
                        )

                    user = get_current_user(
                        access_token
                    )

                    save_login(
                        access_token=access_token,
                        user=user,
                    )

                    try:
                        reports = get_reports(
                            access_token
                        )
                        save_reports(reports)
                    except Exception:
                        save_reports([])

                    st.session_state.current_page = "dashboard"

                    st.rerun()

                except Exception as exc:
                    st.error(str(exc))

    with signup_tab:
        st.subheader("Create your account")

        with st.form("signup_form"):
            name = st.text_input(
                "Name",
                key="signup_name",
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

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm_password",
            )

            submitted = st.form_submit_button(
                "Create Account",
                width="stretch",
            )

        if submitted:
            if not name or not email or not password:
                st.error(
                    "Please fill in all required fields."
                )

            elif len(password) < 8:
                st.error(
                    "Password must be at least 8 characters long."
                )

            elif password != confirm_password:
                st.error(
                    "Passwords do not match."
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

                except Exception as exc:
                    st.error(str(exc))
