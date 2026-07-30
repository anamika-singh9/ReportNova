import streamlit as st


def render_metrics(result: dict) -> None:
    """
    Render report metrics.

    Args:
        result:
            Backend response dictionary.
    """

    report = result.get("report", "")

    word_count = len(report.split())

    character_count = len(report)

    source_count = len(
        result.get("sources", [])
    )

    generation_time = result.get(
        "generation_time",
        "--",
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="📝 Words",
            value=f"{word_count:,}",
        )

    with col2:

        st.metric(
            label="🔤 Characters",
            value=f"{character_count:,}",
        )

    with col3:

        st.metric(
            label="📚 Sources",
            value=source_count,
        )

    with col4:

        st.metric(
            label="⏱ Time",
            value=generation_time,
        )