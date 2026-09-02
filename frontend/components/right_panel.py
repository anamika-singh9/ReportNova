import streamlit as st

from frontend.components.progress import (
    ProgressUI,
)


def render_right_panel(
    placeholder=None,
) -> ProgressUI:
    """
    Render the independent right-side Agent Progress panel.

    Only workflow progress is displayed here.

    No:
    - Recent Reports
    - Project Status
    - Backend Status
    - Version
    """

    if placeholder is None:

        placeholder = st.empty()

    progress_ui = ProgressUI(
        placeholder
    )

    return progress_ui