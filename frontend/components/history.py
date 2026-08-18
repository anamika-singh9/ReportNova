import streamlit as st

from frontend.api.backend import (
    get_report,
    delete_report,
    get_reports,
)

from frontend.services.session import (
    save_reports,
    save_result,
)


def render_history_page():
    """
    Render all reports of current user.
    """

    st.title("📜 Report History")

    reports = st.session_state.history

    if not reports:

        st.info(
            "You have not generated any reports yet."
        )

        return

    for report in reports:

        report_id = report["id"]

        topic = report["topic"]

        created_at = report.get(
            "created_at",
            "",
        )

        citation_style = report.get(
            "citation_style",
            "",
        )

        with st.container():

            st.markdown(
                f"### 📄 {topic}"
            )

            st.caption(
                f"Created: {created_at}"
            )

            st.caption(
                f"Citation Style: {citation_style}"
            )

            col1, col2 = st.columns(2)

            # ==========================================
            # OPEN REPORT
            # ==========================================

            with col1:

                if st.button(
                    "Open",
                    key=f"open_{report_id}",
                    use_container_width=True,
                ):

                    try:

                        selected_report = get_report(
                            report_id=report_id,
                            access_token=(
                                st.session_state
                                .access_token
                            ),
                        )

                        save_result(
                            {
                                "report": (
                                    selected_report.get(
                                        "report_content",
                                        "",
                                    )
                                ),
                                "sources": (
                                    selected_report.get(
                                        "sources",
                                        []
                                    )
                                ),
                                "pdf_path": (
                                    selected_report.get(
                                        "pdf_path",
                                        ""
                                    )
                                ),
                                "topic": (
                                    selected_report.get(
                                        "topic",
                                        ""
                                    )
                                ),
                                "citation_style": (
                                    selected_report.get(
                                        "citation_style",
                                        ""
                                    )
                                ),
                            }
                        )

                        st.session_state.selected_report_id = (
                            report_id
                        )

                        st.session_state.current_page = (
                            "dashboard"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            str(e)
                        )

            # ==========================================
            # DELETE REPORT
            # ==========================================

            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{report_id}",
                    use_container_width=True,
                ):

                    try:

                        delete_report(
                            report_id=report_id,
                            access_token=(
                                st.session_state
                                .access_token
                            ),
                        )

                        updated_reports = get_reports(
                            access_token=(
                                st.session_state
                                .access_token
                            ),
                        )

                        save_reports(
                            updated_reports
                        )

                        st.success(
                            "Report deleted successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            str(e)
                        )

            st.markdown("---")