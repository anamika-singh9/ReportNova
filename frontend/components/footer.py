import streamlit as st


def render_footer():
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("🤖 AI Research Lab")

    with col2:
        st.caption("Powered by LangGraph + RAG")

    with col3:
        st.caption("© 2026 AgentForge")