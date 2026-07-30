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

# ----------------------------------------------------
# Session State
# ----------------------------------------------------

from frontend.services.session import (
    initialize_session,
    save_history,
    save_result,
)

# ----------------------------------------------------
# Page
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Research Lab",
    page_icon="🤖",
    layout="wide",
)

initialize_session()



# ----------------------------------------------------
# CSS
# ----------------------------------------------------

with open("frontend/styles.css") as css:
    content = css.read()
    print(content)
    st.markdown(
        f"<style>{content}</style>",
        unsafe_allow_html=True,
    )
# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

render_sidebar(
    backend_online()
)

# ----------------------------------------------------
# Layout
# ----------------------------------------------------

left, right = st.columns([4, 1])

# ====================================================
# LEFT
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

            with st.spinner("Generating report..."):

                result = generate_report(
                    topic,
                    citation_style,
                    uploaded_file,
                )

                start_time = time.time()

                while True:

                    update = progress_service.get()

                    progress_ui.update(update)

                    timeline_ui.update(update)

                    if update["progress"] >= 100:
                        break

                    if time.time() - start_time > 900:
                        st.error("Workflow timed out.")
                        break

                    time.sleep(0.20)

            if result:

                save_history(topic)

                save_result(result)

                st.success(
                    "✅ Report Generated Successfully"
                )

# ----------------------------------------------------
# Show Result
# ----------------------------------------------------

    if st.session_state.result:

        render_metrics(
            st.session_state.result
        )

        render_report(
            st.session_state.result
        )

# ====================================================
# RIGHT
# ====================================================

with right:

    render_right_panel(
        history=st.session_state.history,
        backend_online=backend_online(),
    )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

render_footer()


