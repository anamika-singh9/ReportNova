import sys
import os
import time

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

from frontend.api.backend import (
    backend_online,
    generate_report,
    get_reports,
)

from frontend.services.progress_service import (
    ProgressService,
)

from frontend.components.sidebar import (
    render_sidebar,
)

from frontend.components.header import (
    render_header,
)

from frontend.components.input_form import (
    render_input_form,
)

from frontend.components.progress import (
    ProgressUI,
)

from frontend.components.timeline import (
    TimelineUI,
)

from frontend.components.metrics import (
    render_metrics,
)

from frontend.components.report import (
    render_report,
)

from frontend.components.right_panel import (
    render_right_panel,
)

from frontend.components.footer import (
    render_footer,
)

from frontend.services.session import (
    initialize_session,
    save_reports,
    save_result,
)

from frontend.components.auth import (
    render_auth_page,
)

from frontend.components.history import (
    render_history_page,
)


# ====================================================
# PAGE CONFIG
# ====================================================

st.set_page_config(
    page_title="AI Research Lab",
    page_icon="🤖",
    layout="wide",
)


# ====================================================
# INITIALIZE SESSION
# ====================================================

initialize_session()


# ====================================================
# AUTHENTICATION CHECK
# ====================================================

if not st.session_state.authenticated:

    render_auth_page()

    st.stop()


# ====================================================
# CSS
# ====================================================

with open("frontend/styles.css") as css:

    content = css.read()

    st.markdown(
        f"<style>{content}</style>",
        unsafe_allow_html=True,
    )


# ====================================================
# SIDEBAR
# ====================================================

render_sidebar(
    backend_online()
)


# ====================================================
# HISTORY PAGE
# ====================================================

if st.session_state.current_page == "history":

    render_history_page()

    render_footer()

    st.stop()


# ====================================================
# DASHBOARD PAGE
# ====================================================

left, right = st.columns([4, 1])


# ====================================================
# LEFT SIDE
# ====================================================

with left:

    render_header()

    (
        topic,
        uploaded_file,
        citation_style,
        generate,
        progress_placeholder,
        timeline_placeholder,
    ) = render_input_form()


    # ==================================================
    # GENERATE REPORT
    # ==================================================

    if generate:

        if not topic.strip():

            st.warning(
                "Please enter a research topic."
            )

        else:

            with progress_placeholder:

                progress_ui = ProgressUI()

            with timeline_placeholder:

                timeline_ui = TimelineUI()

            progress_service = ProgressService()


            with st.spinner(
                "Generating report..."
            ):

                result = generate_report(
                    topic=topic,
                    citation_style=citation_style,
                    access_token=(
                        st.session_state.access_token
                    ),
                    uploaded_file=uploaded_file,
                )

                start_time = time.time()


                # ==========================================
                # PROGRESS POLLING
                # ==========================================

                while True:

                    update = progress_service.get()

                    progress_ui.update(update)

                    timeline_ui.update(update)

                    if update["progress"] >= 100:

                        break

                    if time.time() - start_time > 900:

                        st.error(
                            "Workflow timed out."
                        )

                        break

                    time.sleep(0.20)


            # ==============================================
            # SAVE GENERATED REPORT
            # ==============================================

            if result:

                save_result(result)

                reports = get_reports(
                    st.session_state.access_token
                )

                save_reports(reports)

                st.success(
                    "✅ Report Generated Successfully"
                )


    # ==================================================
    # SHOW CURRENT REPORT
    # ==================================================

    if st.session_state.result:

        render_metrics(
            st.session_state.result
        )

        render_report(
            st.session_state.result
        )


# ====================================================
# RIGHT PANEL
# ====================================================

with right:

    render_right_panel(
        history=st.session_state.history,
        backend_online=backend_online(),
    )


# ====================================================
# FOOTER
# ====================================================

render_footer()