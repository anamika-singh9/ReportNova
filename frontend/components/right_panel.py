import streamlit as st


def render_right_panel(
    history: list,
    backend_online: bool,
) -> None:
    """
    Render the right-side information panel.

    Shows:
    - Recent Reports
    - Project Status
    - Backend Status
    """

    st.markdown("## 📚 Recent Reports")

    if history:

        for item in history:

            st.button(
                f"📄 {item}",
                use_container_width=True,
                disabled=True,
            )

    else:

        st.info(
            "No reports generated yet."
        )

    st.markdown("---")

    st.markdown("## 📊 Project Status")

    st.metric(
        "AI Agents",
        "7",
    )

    st.metric(
        "Workflow",
        "LangGraph",
    )

    st.metric(
        "RAG",
        "Enabled",
    )

    st.metric(
        "Web Search",
        "Enabled",
    )

    if backend_online:

        st.success(
            "🟢 Backend Connected"
        )

    else:

        st.error(
            "🔴 Backend Offline"
        )

    st.markdown("---")

    st.success(
        "✅ AI Research Lab v1.0"
    )