import streamlit as st


def render_sidebar(
    backend_status: bool,
) -> None:
    """
    Render the application sidebar.

    Args:
        backend_status:
            True if backend is online,
            otherwise False.
    """

    with st.sidebar:

        st.title("🤖 AI Research Lab")

        st.markdown("---")

        st.button(
            "🏠 Dashboard",
            use_container_width=True,
            disabled=True,
        )

        st.button(
            "🕒 History",
            use_container_width=True,
            disabled=True,
        )

        st.markdown("---")

        st.caption("Version 1.0")

        st.markdown("---")

        if backend_status:

            st.success(
                "🟢 Backend Connected"
            )

        else:

            st.error(
                "🔴 Backend Offline"
            )

        st.markdown("---")

        st.info("🤖 7 AI Agents")

        st.info("📚 RAG Enabled")

        st.info("🌐 Web Search Enabled")

        st.info("📄 PDF Generation")

        st.markdown("---")

        st.caption(
            "Built with LangGraph + FastAPI + Streamlit"
        )