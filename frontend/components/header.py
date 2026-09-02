import streamlit as st


def render_header():

    st.markdown(
        """
<div class="glass-card">
<div class="main-title">
ReportNova
</div>
<div class="sub-title">
Generate professional, well-structured research reports using <strong>LangGraph</strong>, <strong>RAG</strong>, <strong>Web Search</strong> and <strong>Multi-Agent AI</strong>.<br>
Research, analyze, verify and organize information into publication-ready reports with properly formatted sources.
</div>
</div>
""",
        unsafe_allow_html=True,
    )