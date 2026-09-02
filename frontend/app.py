import os
import sys
import threading
import uuid
import time

import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# ============================================================
# BACKEND API
# ============================================================

from frontend.api.backend import (
    backend_online,
    generate_report,
    get_reports,
)


# ============================================================
# SERVICES
# ============================================================

from frontend.services.session import (
    initialize_session,
    save_reports,
    save_result,
)


# ============================================================
# COMPONENTS
# ============================================================

from frontend.components.sidebar import (
    render_sidebar,
)

from frontend.components.header import (
    render_header,
)

from frontend.components.input_form import (
    render_input_form,
)

from frontend.components.metrics import (
    render_metrics,
)

from frontend.components.report import (
    render_report,
    render_report_page,
)

from frontend.components.footer import (
    render_footer,
)

from frontend.components.auth import (
    render_auth_page,
)

from frontend.components.history import (
    render_history_page,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReportNova",
    page_icon="📘",
    layout="wide",
)


# ============================================================
# SESSION INITIALIZATION
# ============================================================

initialize_session()


# ============================================================
# GLOBAL BACKGROUND JOB STORE
# ============================================================

if not hasattr(
    st,
    "_generation_jobs",
):
    st._generation_jobs = {}


if not hasattr(
    st,
    "_generation_jobs_lock",
):
    st._generation_jobs_lock = threading.Lock()


# ============================================================
# AUTHENTICATION
# ============================================================

if not st.session_state.authenticated:

    render_auth_page()

    st.stop()


# ============================================================
# CSS
# ============================================================

CSS_PATH = os.path.join(
    ROOT_DIR,
    "frontend",
    "styles.css",
)

if os.path.exists(CSS_PATH):

    with open(
        CSS_PATH,
        encoding="utf-8",
    ) as css:

        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True,
        )


# ============================================================
# BACKGROUND GENERATION JOB
# ============================================================

def start_generation_job(
    topic,
    citation_style,
    access_token,
    uploaded_file,
):
    """
    Start report generation in a background thread.

    Background worker does not access Streamlit session state.
    """

    job_id = str(uuid.uuid4())


    # ========================================================
    # COPY UPLOADED FILE DATA BEFORE THREAD
    # ========================================================

    uploaded_file_data = None

    if uploaded_file is not None:

        try:

            uploaded_file_data = {
                "name": uploaded_file.name,
                "data": uploaded_file.getvalue(),
            }

        except Exception:

            uploaded_file_data = None


    # ========================================================
    # CREATE JOB
    # ========================================================

    with st._generation_jobs_lock:

        st._generation_jobs[job_id] = {

            "status": "running",

            "result": None,

            "error": None,

            "created_at": time.time(),

            "completed_at": None,

        }


    # ========================================================
    # WORKER
    # ========================================================

    def worker():

        try:

            file_for_backend = None

            if uploaded_file_data is not None:

                class UploadedFileData:

                    def __init__(
                        self,
                        name,
                        data,
                    ):
                        self.name = name
                        self._data = data

                    def getvalue(self):
                        return self._data


                file_for_backend = UploadedFileData(
                    uploaded_file_data["name"],
                    uploaded_file_data["data"],
                )


            # ------------------------------------------------
            # CALL BACKEND
            # ------------------------------------------------

            result = generate_report(

                topic=topic,

                citation_style=citation_style,

                access_token=access_token,

                uploaded_file=file_for_backend,

            )


            # ------------------------------------------------
            # VALIDATE RESULT
            # ------------------------------------------------

            if not isinstance(
                result,
                dict,
            ):

                raise RuntimeError(
                    "Backend returned an invalid report response."
                )


            # ------------------------------------------------
            # STORE RESULT
            # ------------------------------------------------

            with st._generation_jobs_lock:

                existing = st._generation_jobs.get(
                    job_id,
                    {},
                )

                st._generation_jobs[job_id] = {

                    "status": "completed",

                    "result": result,

                    "error": None,

                    "created_at": existing.get(
                        "created_at",
                        time.time(),
                    ),

                    "completed_at": time.time(),

                }


        except Exception as e:

            with st._generation_jobs_lock:

                existing = st._generation_jobs.get(
                    job_id,
                    {},
                )

                st._generation_jobs[job_id] = {

                    "status": "failed",

                    "result": None,

                    "error": str(e),

                    "created_at": existing.get(
                        "created_at",
                        time.time(),
                    ),

                    "completed_at": time.time(),

                }


    # ========================================================
    # START THREAD
    # ========================================================

    thread = threading.Thread(
        target=worker,
        daemon=True,
        name=f"report-generation-{job_id}",
    )

    thread.start()

    return job_id


# ============================================================
# GENERATION MONITOR
# ============================================================

@st.fragment(run_every=0.5)
def monitor_generation():

    if not st.session_state.get(
        "generation_running",
        False,
    ):
        return


    job_id = st.session_state.get(
        "generation_job_id"
    )

    if not job_id:
        return


    # ========================================================
    # READ JOB
    # ========================================================

    with st._generation_jobs_lock:

        job = st._generation_jobs.get(
            job_id
        )

        if job is not None:
            job = dict(job)


    if not job:
        return


    status = job.get(
        "status",
        "running",
    )


    # ========================================================
    # RUNNING
    # ========================================================

    if status == "running":

        st.info(
            "🔄 Generating research report..."
        )

        st.caption(
            "⚡ Research agents are working. "
            "Please wait until the report is generated."
        )

        return


    # ========================================================
    # FAILED
    # ========================================================

    if status == "failed":

        error = job.get(
            "error",
            "Report generation failed.",
        )

        st.session_state.generation_running = False

        st.session_state.generation_error = error

        st.session_state.generation_job_id = None

        st.session_state.agent_progress = {}

        with st._generation_jobs_lock:

            st._generation_jobs.pop(
                job_id,
                None,
            )

        st.rerun()

        return


    # ========================================================
    # COMPLETED
    # ========================================================

    if status == "completed":

        result = job.get(
            "result"
        )


        # ----------------------------------------------------
        # EMPTY RESULT PROTECTION
        # ----------------------------------------------------

        if not result:

            st.session_state.generation_running = False

            st.session_state.generation_error = (
                "Backend completed the request "
                "but returned an empty report."
            )

            st.session_state.generation_job_id = None

            with st._generation_jobs_lock:

                st._generation_jobs.pop(
                    job_id,
                    None,
                )

            st.rerun()

            return


        # ====================================================
        # SAVE GENERATED RESULT
        # ====================================================

        try:

            save_result(
                result
            )

        except Exception as e:

            st.session_state.generation_running = False

            st.session_state.generation_error = (
                f"Report was generated, but could not "
                f"be displayed: {e}"
            )

            st.session_state.generation_job_id = None

            with st._generation_jobs_lock:

                st._generation_jobs.pop(
                    job_id,
                    None,
                )

            st.rerun()

            return


        # ====================================================
        # REFRESH HISTORY
        # ====================================================

        history_error = None

        try:

            reports = get_reports(
                st.session_state.access_token
            )

            save_reports(
                reports
            )

        except PermissionError:

            st.session_state.generation_running = False

            st.session_state.generation_error = (
                "Your session has expired. "
                "Please login again."
            )

            st.session_state.generation_job_id = None

            with st._generation_jobs_lock:

                st._generation_jobs.pop(
                    job_id,
                    None,
                )

            st.rerun()

            return

        except Exception as e:

            history_error = str(e)


        # ====================================================
        # GENERATION COMPLETED
        # ====================================================

        st.session_state.generation_running = False

        st.session_state.generation_result = result

        st.session_state.generation_job_id = None


        # ====================================================
        # FINAL PROGRESS
        # ====================================================

        current_progress = st.session_state.get(
            "agent_progress",
            {},
        )

        if not isinstance(
            current_progress,
            dict,
        ):
            current_progress = {}


        current_progress.update({

            "workflow": "Completed",

            "status": "completed",

            "progress": 100,

        })


        st.session_state.agent_progress = (
            current_progress
        )


        # ====================================================
        # HISTORY WARNING
        # ====================================================

        if history_error:

            st.session_state.generation_error = (
                "Report generated successfully, "
                "but history could not refresh: "
                f"{history_error}"
            )


        # ====================================================
        # REMOVE JOB
        # ====================================================

        with st._generation_jobs_lock:

            st._generation_jobs.pop(
                job_id,
                None,
            )


        # ====================================================
        # RERUN
        # ====================================================

        st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar(
    backend_online()
)


# ============================================================
# HISTORY PAGE
# ============================================================

if (
    st.session_state.current_page
    == "history"
):

    render_history_page()

    render_footer()

    st.stop()


# ============================================================
# SAVED REPORT PAGE
# ============================================================

if (
    st.session_state.current_page
    == "report"
):

    render_report_page()

    render_footer()

    st.stop()


# ============================================================
# DASHBOARD
# ============================================================

render_header()


# ============================================================
# INPUT FORM
# ============================================================

(
    topic,
    uploaded_file,
    citation_style,
    generate,
) = render_input_form()


# ============================================================
# START GENERATION
# ============================================================

if (
    generate
    and not st.session_state.get(
        "generation_running",
        False,
    )
):

    if not topic.strip():

        st.warning(
            "Please enter a research topic."
        )

        st.stop()


    # ========================================================
    # RESET PREVIOUS GENERATION
    # ========================================================

    st.session_state.generation_error = None

    st.session_state.generation_result = None

    st.session_state.result = None

    st.session_state.selected_report_id = None

    st.session_state.agent_progress = {}

    st.session_state.generation_start_time = time.time()


    # ========================================================
    # START BACKGROUND JOB
    # ========================================================

    job_id = start_generation_job(

        topic=topic,

        citation_style=citation_style,

        access_token=(
            st.session_state.access_token
        ),

        uploaded_file=uploaded_file,

    )


    st.session_state.generation_job_id = (
        job_id
    )

    st.session_state.generation_running = True


    st.rerun()


# ============================================================
# GENERATION MONITOR
# ============================================================

monitor_generation()


# ============================================================
# GENERATION ERROR
# ============================================================

if st.session_state.get(
    "generation_error"
):

    st.error(
        st.session_state.generation_error
    )


# ============================================================
# CURRENT REPORT
# ============================================================

current_result = st.session_state.get(
    "result"
)


if current_result:

    st.markdown("---")


    # ========================================================
    # METRICS
    # ========================================================

    render_metrics(
        current_result
    )


    # ========================================================
    # REPORT / SOURCES / DOWNLOAD
    # ========================================================

    render_report(
        current_result
    )


# ============================================================
# FOOTER
# ============================================================

render_footer()