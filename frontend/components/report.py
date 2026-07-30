import os

import streamlit as st


def render_report(result: dict) -> None:
    """
    Render the generated report.

    Responsibilities:
    - Report tab
    - Sources tab
    - Download tab
    """

    tab1, tab2, tab3 = st.tabs(
        [
            "📄 Research Report",
            "📚 Sources",
            "📥 Download",
        ]
    )

    # ==========================================================
    # REPORT
    # ==========================================================

    with tab1:

        st.markdown(
            "## 📄 Generated Research Report"
        )

        st.divider()

        st.markdown(
            result.get(
                "report",
                "No report generated.",
            )
        )

    # ==========================================================
    # SOURCES
    # ==========================================================

    with tab2:

        sources = result.get(
            "sources",
            [],
        )

        if not sources:

            st.info(
                "No sources available."
            )

        else:

            st.markdown(
                "## 📚 Research Sources"
            )

            st.divider()

            for i, source in enumerate(
                sources,
                start=1,
            ):

                title = source.get(
                    "title",
                    "Unknown Source",
                )

                url = source.get(
                    "url",
                    "",
                )

                with st.expander(
                    f"{i}. {title}"
                ):

                    st.write(
                        "**Title**"
                    )

                    st.write(title)

                    if url:

                        st.write(
                            "**URL**"
                        )

                        st.link_button(
                            "Open Source",
                            url,
                        )

    # ==========================================================
    # DOWNLOAD
    # ==========================================================

    with tab3:

        pdf_path = result.get(
            "pdf_path",
            "",
        )

        if (
            pdf_path
            and os.path.exists(pdf_path)
        ):

            st.success(
                "Your report is ready."
            )

            st.caption(
                "Download the generated PDF."
            )

            with open(
                pdf_path,
                "rb",
            ) as pdf:

                st.download_button(
                    label="⬇ Download PDF",
                    data=pdf,
                    file_name="AI_Research_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        else:

            st.warning(
                "PDF not available."
            )