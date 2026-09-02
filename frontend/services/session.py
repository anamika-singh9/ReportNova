import streamlit as st


# ============================================================
# INITIALIZE SESSION
# ============================================================

def initialize_session():

    defaults = {

        # AUTH
        "access_token": None,

        "user": None,

        "authenticated": False,


        # NAVIGATION
        "current_page": "dashboard",

        "selected_report_id": None,


        # REPORTS
        "history": [],

        "result": None,

        "report": "",

        "sources": [],

        "pdf_path": "",


        # WORKFLOW
        "running": False,

        "progress": 0,

        "current_agent": "",

        "execution_time": 0,


        # AGENT PROGRESS
        "agent_progress": {},


        # GENERATION
        "generation_running": False,

        "generation_result": None,

        "generation_error": None,

        "generation_start_time": None,

        "generation_job_id": None,

    }


    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ============================================================
# LOGIN
# ============================================================

def save_login(
    access_token: str,
    user: dict | None = None,
):

    st.session_state.access_token = (
        access_token
    )

    st.session_state.user = user

    st.session_state.authenticated = True


    # ========================================================
    # NAVIGATION
    # ========================================================

    st.session_state.current_page = (
        "dashboard"
    )

    st.session_state.selected_report_id = (
        None
    )


    # ========================================================
    # CURRENT REPORT
    # ========================================================

    st.session_state.result = None

    st.session_state.report = ""

    st.session_state.sources = []

    st.session_state.pdf_path = ""


    # ========================================================
    # WORKFLOW
    # ========================================================

    st.session_state.running = False

    st.session_state.progress = 0

    st.session_state.current_agent = ""

    st.session_state.execution_time = 0

    st.session_state.agent_progress = {}


    # ========================================================
    # GENERATION
    # ========================================================

    st.session_state.generation_running = False

    st.session_state.generation_result = None

    st.session_state.generation_error = None

    st.session_state.generation_start_time = None

    st.session_state.generation_job_id = None


# ============================================================
# LOGOUT
# ============================================================

def logout():

    st.session_state.access_token = None

    st.session_state.user = None

    st.session_state.authenticated = False


    st.session_state.current_page = (
        "dashboard"
    )

    st.session_state.selected_report_id = (
        None
    )


    st.session_state.history = []

    st.session_state.result = None

    st.session_state.report = ""

    st.session_state.sources = []

    st.session_state.pdf_path = ""


    st.session_state.running = False

    st.session_state.progress = 0

    st.session_state.current_agent = ""

    st.session_state.execution_time = 0

    st.session_state.agent_progress = {}


    st.session_state.generation_running = False

    st.session_state.generation_result = None

    st.session_state.generation_error = None

    st.session_state.generation_start_time = None

    st.session_state.generation_job_id = None


# ============================================================
# SAVE REPORTS
# ============================================================

def save_reports(
    reports: list,
):

    if not isinstance(
        reports,
        list,
    ):

        reports = []


    normalized_reports = []


    for report in reports:

        if not isinstance(
            report,
            dict,
        ):

            continue


        report_id = report.get(
            "id",
            report.get("report_id"),
        )


        report_content = report.get(
            "report_content",
            report.get(
                "report",
                "",
            ),
        )


        normalized_reports.append({

            "id": report_id,

            "report_id": report_id,

            "topic": report.get(
                "topic",
                "Untitled Report",
            ),

            "citation_style": report.get(
                "citation_style",
                "",
            ),

            "report_content":
                report_content or "",

            "report":
                report_content or "",

            "sources": report.get(
                "sources",
                [],
            ) or [],

            "pdf_path": report.get(
                "pdf_path",
                "",
            ) or "",

            "generation_time": report.get(
                "generation_time",
                "--",
            ),

            "created_at": report.get(
                "created_at"
            ),

        })


    st.session_state.history = (
        normalized_reports
    )


# ============================================================
# SAVE RESULT
# ============================================================

def save_result(
    result: dict,
):

    if not isinstance(
        result,
        dict,
    ):

        raise ValueError(
            "Invalid report result received."
        )


    normalized = dict(
        result
    )


    # ========================================================
    # REPORT CONTENT
    # ========================================================

    report_content = normalized.get(
        "report_content"
    )


    if not report_content:

        report_content = normalized.get(
            "report",
            "",
        )


    if report_content is None:

        report_content = ""


    report_content = str(
        report_content
    )


    normalized["report_content"] = (
        report_content
    )

    normalized["report"] = (
        report_content
    )


    # ========================================================
    # SOURCES
    # ========================================================

    sources = normalized.get(
        "sources",
        [],
    )


    if sources is None:

        sources = []


    normalized["sources"] = sources


    # ========================================================
    # PDF
    # ========================================================

    pdf_path = normalized.get(
        "pdf_path",
        "",
    )


    if pdf_path is None:

        pdf_path = ""


    normalized["pdf_path"] = str(
        pdf_path
    )


    # ========================================================
    # IDS
    # ========================================================

    report_id = normalized.get(
        "report_id",
        normalized.get("id"),
    )


    if report_id is not None:

        normalized["report_id"] = (
            report_id
        )

        normalized["id"] = (
            report_id
        )


    # ========================================================
    # SAVE
    # ========================================================

    st.session_state.result = (
        normalized
    )

    st.session_state.generation_result = (
        normalized
    )

    st.session_state.report = (
        report_content
    )

    st.session_state.sources = (
        sources
    )

    st.session_state.pdf_path = (
        normalized["pdf_path"]
    )


# ============================================================
# ADD REPORT TO HISTORY
# ============================================================

def add_report_to_history(
    report: dict,
):

    if not isinstance(
        report,
        dict,
    ):

        return


    report_id = report.get(
        "report_id",
        report.get("id"),
    )


    report_content = report.get(
        "report_content",
        report.get(
            "report",
            "",
        ),
    )


    new_item = {

        "id": report_id,

        "report_id": report_id,

        "topic": report.get(
            "topic",
            "Untitled Report",
        ),

        "citation_style": report.get(
            "citation_style",
            "",
        ),

        "report_content":
            report_content or "",

        "report":
            report_content or "",

        "sources": report.get(
            "sources",
            [],
        ) or [],

        "pdf_path": report.get(
            "pdf_path",
            "",
        ) or "",

        "generation_time": report.get(
            "generation_time",
            "--",
        ),

        "created_at": report.get(
            "created_at"
        ),

    }


    # ========================================================
    # REMOVE DUPLICATE
    # ========================================================

    if report_id is not None:

        st.session_state.history = [

            item

            for item in st.session_state.history

            if (
                item.get("id")
                != report_id

                and

                item.get("report_id")
                != report_id
            )

        ]


    # ========================================================
    # INSERT FIRST
    # ========================================================

    st.session_state.history.insert(
        0,
        new_item,
    )

# ============================================================
# RESET AGENT PROGRESS
# ============================================================

def reset_agent_progress():
    """
    Reset the agent tracker when navigating away
    from a completed generation.
    """

    st.session_state.agent_progress = {}

    st.session_state.progress = 0

    st.session_state.current_agent = ""

    st.session_state.execution_time = 0

    st.session_state.running = False