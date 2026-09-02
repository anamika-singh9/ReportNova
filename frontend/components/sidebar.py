import os

import streamlit as st

from frontend.services.progress_service import (
    ProgressService,
)

from frontend.services.session import (
    save_result,
    reset_agent_progress,
    logout,
)


# ============================================================
# AGENT PROGRESS
# ============================================================

@st.fragment(run_every=0.5)
def render_agent_progress():

    AGENTS = [

        "Planner",
        "Research",
        "Fact Checker",
        "Writer",
        "Citation",
        "Reviewer",
        "PDF Generator",

    ]

    # ========================================================
    # PROGRESS SOURCE
    # ========================================================

    generation_running = st.session_state.get(
        "generation_running",
        False,
    )

    if generation_running:

        progress_service = ProgressService(
            interval=0.2
        )

        live_data = progress_service.get()

        if isinstance(
            live_data,
            dict,
        ):

            st.session_state.agent_progress = (
                live_data
            )

            progress_data = live_data

        else:

            progress_data = (
                st.session_state.get(
                    "agent_progress",
                    {},
                )
            )

    else:

        progress_data = (
            st.session_state.get(
                "agent_progress",
                {},
            )
        )

    if not isinstance(
        progress_data,
        dict,
    ):

        progress_data = {}

    # ========================================================
    # PANEL
    # ========================================================

    with st.expander(
        "⚡ Agent Progress",
        expanded=False,
    ):

        agent_states = {

            agent: {

                "status": "Pending",

                "time": "—",

            }

            for agent in AGENTS

        }

        # ====================================================
        # BACKEND HISTORY
        # ====================================================

        history = progress_data.get(
            "history",
            [],
        )

        if not isinstance(
            history,
            list,
        ):

            history = []

        for item in history:

            if not isinstance(
                item,
                dict,
            ):
                continue

            node = item.get(
                "node",
                "",
            )

            if node not in agent_states:
                continue

            status = str(
                item.get(
                    "status",
                    "pending",
                )
            ).lower()

            node_time = item.get(
                "node_time",
                "—",
            )

            if status == "completed":

                agent_states[node] = {

                    "status": "Completed",

                    "time": node_time,

                }

            elif status == "failed":

                agent_states[node] = {

                    "status": "Failed",

                    "time": node_time,

                }

            elif status == "running":

                agent_states[node] = {

                    "status": "Running",

                    "time": node_time,

                }

        # ====================================================
        # CURRENT NODE
        # ====================================================

        current_node = progress_data.get(
            "node",
            "",
        )

        current_status = str(
            progress_data.get(
                "status",
                "idle",
            )
        ).lower()

        if current_node in agent_states:

            node_time = progress_data.get(
                "node_time",
                "0.00s",
            )

            if current_status == "running":

                agent_states[current_node] = {

                    "status": "Running",

                    "time": node_time,

                }

            elif current_status == "completed":

                agent_states[current_node] = {

                    "status": "Completed",

                    "time": node_time,

                }

            elif current_status == "failed":

                agent_states[current_node] = {

                    "status": "Failed",

                    "time": node_time,

                }

        # ====================================================
        # RENDER HELPER
        # ====================================================

        def render_agent(agent):

            data = agent_states[agent]

            status = data["status"]

            execution_time = data["time"]

            if status == "Completed":

                icon = "✓"

            elif status == "Running":

                icon = "🔄"

            elif status == "Failed":

                icon = "✗"

            else:

                icon = "○"

            st.markdown(
                f"**{icon} {agent}**"
            )

            st.caption(
                f"{status} • ⏱ {execution_time}"
            )

        # ====================================================
        # FIRST 6 AGENTS
        # ====================================================

        for row_start in range(
            0,
            6,
            2,
        ):

            row_agents = AGENTS[
                row_start:row_start + 2
            ]

            columns = st.columns(
                2,
                gap="small",
            )

            for index, agent in enumerate(
                row_agents
            ):

                with columns[index]:

                    render_agent(agent)

        # ====================================================
        # PDF GENERATOR
        # ====================================================

        left, center, right = st.columns(
            [1, 2, 1]
        )

        with center:

            render_agent(
                "PDF Generator"
            )

        # ====================================================
        # OVERALL PROGRESS
        # ====================================================

        progress_value = progress_data.get(
            "progress",
            0,
        )

        try:

            progress_value = float(
                progress_value
            )

        except (
            ValueError,
            TypeError,
        ):

            progress_value = 0

        progress_value = max(
            0,
            min(
                100,
                progress_value,
            ),
        )

        st.markdown("---")

        st.markdown(
            f"**Overall Progress** — "
            f"{progress_value:.0f}%"
        )

        st.progress(
            progress_value / 100
        )

        workflow_time = progress_data.get(
            "workflow_time",
            "0.00s",
        )

        st.caption(
            "⏱ Total Workflow Time: "
            f"{workflow_time or '—'}"
        )


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar(
    backend_status: bool,
) -> None:

    with st.sidebar:

        # ====================================================
        # BRANDING
        # ====================================================

        logo_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "assets",
                "reportnova_logo.png",
            )
        )

        if os.path.exists(logo_path):

            st.image(
                logo_path,
                width="stretch",
            )

        else:

            st.title(
                "ReportNova"
            )

        st.caption(
            "Multi-Agent Research Report Generator"
        )

        st.markdown("---")

        # ====================================================
        # USER
        # ====================================================

        user = st.session_state.get(
            "user"
        )

        if user:

            user_name = user.get(
                "name",
                "User",
            )

            user_email = user.get(
                "email",
                "",
            )

            st.caption(
                "LOGGED IN AS"
            )

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

        # ====================================================
        # AGENT PROGRESS
        # ====================================================

        render_agent_progress()

        # ====================================================
        # NAVIGATION
        # ====================================================

        if st.button(
            "🏠 Dashboard",
            width="stretch",
        ):

            st.session_state.current_page = (
                "dashboard"
            )

            # ----------------------------------------------
            # Reset old tracker only when generation
            # is NOT currently running.
            # ----------------------------------------------

            if not st.session_state.get(
                "generation_running",
                False,
            ):

                reset_agent_progress()

                st.session_state.selected_report_id = None

                st.session_state.result = None

                st.session_state.report = ""

                st.session_state.sources = []

                st.session_state.pdf_path = ""

            st.rerun()

        # ====================================================
        # HISTORY
        # ====================================================

        if st.button(
            "🕒 History",
            width="stretch",
        ):

            # ----------------------------------------------
            # Keep active generation on Dashboard.
            # ----------------------------------------------

            if st.session_state.get(
                "generation_running",
                False,
            ):

                st.session_state.current_page = (
                    "dashboard"
                )

                st.info(
                    "Report generation is running on the Dashboard. "
                    "Please stay there until it finishes."
                )

            else:

                # ------------------------------------------
                # Generation finished.
                # Clear old Agent Progress.
                # ------------------------------------------

                reset_agent_progress()

                st.session_state.current_page = (
                    "history"
                )

            st.rerun()

        # ====================================================
        # LOGOUT
        # ====================================================

        st.markdown("---")

        if st.button(
            "🚪 Logout",
            width="stretch",
        ):

            logout()

            st.rerun()

        # ====================================================
        # BACKEND STATUS
        # ====================================================

        st.markdown("---")

        if backend_status:

            st.success(
                "🟢 Backend Connected"
            )

        else:

            st.error(
                "🔴 Backend Offline"
            )

        # ====================================================
        # INFO
        # ====================================================

        st.markdown("---")

        st.info(
            "🤖 7 AI Agents"
        )

        st.info(
            "📚 RAG Enabled"
        )

        st.info(
            "🌐 Web Search Enabled"
        )

        st.info(
            "📄 PDF Generation"
        )

        # ====================================================
        # VERSION
        # ====================================================

        st.markdown("---")

        st.caption(
            "Version 1.0"
        )

        st.caption(
            "Built with LangGraph + FastAPI + Streamlit"
        )