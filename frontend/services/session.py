import streamlit as st


def initialize_session():
    """
    Initialize Streamlit session variables.
    """

    defaults = {
        "history": [],
        "result": None,
        "report": "",
        "sources": [],
        "pdf_path": "",
        "running": False,
        "progress": 0,
        "current_agent": "",
        "execution_time": 0,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


def save_history(topic: str):
    """
    Save recently generated topics.
    """

    if topic not in st.session_state.history:

        st.session_state.history.insert(
            0,
            topic,
        )

    st.session_state.history = st.session_state.history[:10]


def save_result(result: dict):
    """
    Save latest report.
    """

    st.session_state.result = result

    st.session_state.report = result.get(
        "report",
        "",
    )

    st.session_state.sources = result.get(
        "sources",
        [],
    )

    st.session_state.pdf_path = result.get(
        "pdf_path",
        "",
    )