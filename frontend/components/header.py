import streamlit as st


def render_header():

    st.markdown(
        """
<div class="glass-card">
<div class="main-title">
🤖 AI Research Report Generator
</div>
<div class="sub-title">
Generate professional research reports using <strong>LangGraph</strong>, <strong>RAG</strong>, <strong>Web Search</strong> and <strong>Multi-Agent AI</strong>.
</div>
</div>
""",
        unsafe_allow_html=True,
    )