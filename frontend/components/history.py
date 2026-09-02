import streamlit as st

from frontend.api.backend import (
    delete_report,
    get_report,
    get_reports,
)

from frontend.services.session import (
    save_reports,
    save_result,
)


# ============================================================
# OPEN REPORT
# ============================================================

def _open_report(
    report_id: int,
):
    """
    Fetch the complete saved report and open it
    on the separate Report page.
    """

    selected_report = get_report(
        report_id=int(report_id),
        access_token=st.session_state.access_token,
    )


    if not isinstance(
        selected_report,
        dict,
    ):

        raise RuntimeError(
            "Invalid report received from backend."
        )


    report_content = (
        selected_report.get(
            "report_content"
        )
        or selected_report.get(
            "report",
            "",
        )
    )


    save_result({

        "id": report_id,

        "report_id": report_id,

        "topic": selected_report.get(
            "topic",
            "Untitled Report",
        ),

        "citation_style": selected_report.get(
            "citation_style",
            "",
        ),

        "report_content": report_content,

        "report": report_content,

        "sources": selected_report.get(
            "sources",
            [],
        ) or [],

        "pdf_path": selected_report.get(
            "pdf_path",
            "",
        ) or [],

        "generation_time": selected_report.get(
            "generation_time",
            "--",
        ),

        "created_at": selected_report.get(
            "created_at"
        ),

    })


    st.session_state.selected_report_id = (
        int(report_id)
    )


    # IMPORTANT:
    # Open saved report on separate page.
    st.session_state.current_page = (
        "report"
    )


    st.session_state.generation_running = False


    st.rerun()


# ============================================================
# HISTORY PAGE
# ============================================================

def render_history_page():

    st.title(
        "📜 Report History"
    )

    st.caption(
        "Open a saved report without replacing the Dashboard."
    )


    access_token = st.session_state.get(
        "access_token"
    )


    if not access_token:

        st.error(
            "Please login again."
        )

        return


    # ========================================================
    # DATABASE IS SOURCE OF TRUTH
    # ========================================================

    try:

        reports = get_reports(
            access_token
        )

        save_reports(
            reports
        )

    except PermissionError:

        st.error(
            "Your session has expired. Please login again."
        )

        return

    except Exception as exc:

        st.error(
            f"Unable to load report history: {exc}"
        )

        reports = st.session_state.get(
            "history",
            []
        )


    if not reports:

        st.info(
            "No reports have been generated yet."
        )

        return


    # ========================================================
    # REPORT LIST
    # ========================================================

    for index, report in enumerate(
        reports
    ):

        if not isinstance(
            report,
            dict,
        ):

            continue


        report_id = report.get(
            "id",
            report.get("report_id"),
        )


        if report_id is None:

            continue


        topic = str(
            report.get(
                "topic",
                "Untitled Report",
            )
            or "Untitled Report"
        )


        citation_style = str(
            report.get(
                "citation_style",
                "",
            )
            or ""
        )


        created_at = report.get(
            "created_at",
            "",
        )


        with st.container(
            border=True
        ):

            st.subheader(
                topic
            )


            meta = []


            if citation_style:

                meta.append(
                    f"Citation: {citation_style}"
                )


            if created_at:

                meta.append(
                    f"Created: {created_at}"
                )


            if meta:

                st.caption(
                    " • ".join(meta)
                )


            open_col, delete_col = st.columns(
                [4, 1]
            )


            with open_col:

                if st.button(
                    "📄 Open Report",
                    key=f"history_open_{report_id}_{index}",
                    width="stretch",
                ):

                    try:

                        _open_report(
                            int(report_id)
                        )

                    except PermissionError:

                        st.error(
                            "Your session has expired. "
                            "Please login again."
                        )

                    except Exception as exc:

                        st.error(
                            f"Unable to open report: {exc}"
                        )


            with delete_col:

                if st.button(
                    "🗑️ Delete",
                    key=f"history_delete_{report_id}_{index}",
                    width="stretch",
                ):

                    try:

                        delete_report(
                            report_id=int(
                                report_id
                            ),
                            access_token=access_token,
                        )


                        refreshed = get_reports(
                            access_token
                        )


                        save_reports(
                            refreshed
                        )


                        if (
                            st.session_state.get(
                                "selected_report_id"
                            )
                            == int(report_id)
                        ):

                            st.session_state.selected_report_id = None

                            st.session_state.result = None


                        st.rerun()


                    except PermissionError:

                        st.error(
                            "Your session has expired. "
                            "Please login again."
                        )


                    except Exception as exc:

                        st.error(
                            f"Unable to delete report: {exc}"
                        )