import streamlit as st


# ==================================================
# INITIALIZE SESSION
# ==================================================

def initialize_session():
    """
    Initialize all Streamlit session variables.
    """

    defaults = {
        # Authentication
        "access_token": None,
        "user": None,
        "authenticated": False,

        # Navigation
        "current_page": "dashboard",
        "selected_report_id": None,

        # Reports
        "history": [],
        "result": None,
        "report": "",
        "sources": [],
        "pdf_path": "",

        # Workflow
        "running": False,
        "progress": 0,
        "current_agent": "",
        "execution_time": 0,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ==================================================
# LOGIN
# ==================================================

def save_login(
    access_token: str,
    user: dict | None = None,
):
    """
    Save authenticated user session.
    """

    st.session_state.access_token = access_token
    st.session_state.user = user
    st.session_state.authenticated = True


# ==================================================
# LOGOUT
# ==================================================

def logout():
    """
    Clear authenticated user session.
    """

    st.session_state.access_token = None
    st.session_state.user = None
    st.session_state.authenticated = False

    # Clear reports
    st.session_state.history = []
    st.session_state.result = None
    st.session_state.report = ""
    st.session_state.sources = []
    st.session_state.pdf_path = ""

    # Reset workflow state
    st.session_state.running = False
    st.session_state.progress = 0
    st.session_state.current_agent = ""
    st.session_state.execution_time = 0


# ==================================================
# SAVE ALL REPORTS
# ==================================================

def save_reports(
    reports: list,
):
    """
    Save reports fetched from the backend database.
    """

    st.session_state.history = reports


# ==================================================
# SAVE NEWLY GENERATED REPORT
# ==================================================

def save_result(
    result: dict,
):
    """
    Save the currently opened/generated report.
    """

    st.session_state.result = result

    st.session_state.report = result.get(
        "report",
        result.get(
            "report_content",
            "",
        ),
    )

    st.session_state.sources = result.get(
        "sources",
        [],
    )

    st.session_state.pdf_path = result.get(
        "pdf_path",
        "",
    )


# ==================================================
# ADD NEW REPORT TO HISTORY
# ==================================================

def add_report_to_history(
    report: dict,
):
    """
    Add a newly generated report to the
    beginning of the local history.

    The backend/database remains the
    permanent source of truth.
    """

    report_id = report.get("report_id")

    # Avoid duplicate report IDs
    if report_id is not None:

        st.session_state.history = [
            item
            for item in st.session_state.history
            if item.get("id") != report_id
        ]

    # Add newest report at the top
    st.session_state.history.insert(
        0,
        {
            "id": report_id,
            "topic": report.get(
                "topic",
                "",
            ),
            "citation_style": report.get(
                "citation_style",
                "",
            ),
            "report_content": report.get(
                "report",
                "",
            ),
            "sources": report.get(
                "sources",
                [],
            ),
            "pdf_path": report.get(
                "pdf_path",
                "",
            ),
        },
    )