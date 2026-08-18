import streamlit as st

from frontend.services.session import (
    logout,
)


def render_sidebar(
    backend_status: bool,
) -> None:

    with st.sidebar:

        # ==========================================
        # APP TITLE
        # ==========================================

        st.title("🤖 AI Research Lab")

        st.markdown("---")


        # ==========================================
        # LOGGED-IN USER
        # ==========================================

        user = st.session_state.user

        if user:

            user_name = user.get(
                "name",
                "User",
            )

            user_email = user.get(
                "email",
                "",
            )

            st.caption("LOGGED IN AS")

            st.write(
                f"👤 **{user_name}**"
            )

            if user_email:

                st.caption(
                    user_email
                )

        else:

            st.caption(
                "👤 Logged in"
            )

        st.markdown("---")


        # ==========================================
        # NAVIGATION
        # ==========================================

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
        ):

            st.session_state.current_page = (
                "dashboard"
            )

            st.rerun()


        if st.button(
            "🕒 History",
            use_container_width=True,
        ):

            st.session_state.current_page = (
                "history"
            )

            st.rerun()


        # ==========================================
        # LOGOUT
        # ==========================================

        st.markdown("---")

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):

            logout()

            st.rerun()


        # ==========================================
        # BACKEND STATUS
        # ==========================================

        st.markdown("---")

        if backend_status:

            st.success(
                "🟢 Backend Connected"
            )

        else:

            st.error(
                "🔴 Backend Offline"
            )


        # ==========================================
        # APP INFO
        # ==========================================

        st.markdown("---")

        st.info("🤖 7 AI Agents")
        st.info("📚 RAG Enabled")
        st.info("🌐 Web Search Enabled")
        st.info("📄 PDF Generation")


        # ==========================================
        # VERSION
        # ==========================================

        st.markdown("---")

        st.caption(
            "Version 1.0"
        )

        st.caption(
            "Built with LangGraph + FastAPI + Streamlit"
        )