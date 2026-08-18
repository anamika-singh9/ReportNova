import ast
import os
import re

import streamlit as st


# ==============================================================
# URL HELPER
# ==============================================================


def clean_url(url) -> str:
    """
    Convert Markdown-style URLs into normal URLs.

    Example:
        [https://example.com](https://example.com)

    becomes:
        https://example.com
    """

    if not url:
        return ""

    if not isinstance(url, str):
        return ""

    url = url.strip()

    # Markdown URL:
    # [text](https://example.com)
    match = re.match(
        r"^\[.*?\]\((https?://[^)]+)\)$",
        url,
    )

    if match:
        return match.group(1)

    return url


# ==============================================================
# PARSE SERIALIZED SOURCES
# ==============================================================


def parse_serialized_sources(sources):
    """
    Handle sources that were accidentally stored as a string.

    Example:

        "[{'title': 'Example', 'url': 'https://example.com'}]"

    becomes:

        [
            {
                "title": "Example",
                "url": "https://example.com"
            }
        ]
    """

    # ----------------------------------------------------------
    # Case 1: String containing a Python list/dict
    # ----------------------------------------------------------

    if isinstance(sources, str):

        value = sources.strip()

        # Try to parse strings like:
        #
        # "[{'title': '...', 'url': '...'}]"
        #
        # or:
        #
        # "{'title': '...', 'url': '...'}"

        if (
            value.startswith("[")
            or value.startswith("{")
        ):

            try:

                parsed = ast.literal_eval(
                    value
                )

                return parsed

            except (
                ValueError,
                SyntaxError,
            ):

                # Not a valid serialized Python object.
                return sources

        return sources

    # ----------------------------------------------------------
    # Case 2: List containing one serialized list
    # ----------------------------------------------------------

    if isinstance(
        sources,
        list,
    ):

        # Example:
        #
        # [
        #     "[{'title': '...', 'url': '...'}]"
        # ]

        if len(sources) == 1:

            first_item = sources[0]

            if isinstance(
                first_item,
                str,
            ):

                parsed = parse_serialized_sources(
                    first_item
                )

                # If parsing produced a list,
                # return that list directly.
                if isinstance(
                    parsed,
                    list,
                ):

                    return parsed

                # If parsing produced a dictionary,
                # wrap it into a list.
                if isinstance(
                    parsed,
                    dict,
                ):

                    return [parsed]

        return sources

    return sources


# ==============================================================
# SOURCE NORMALIZATION
# ==============================================================


def normalize_source(source) -> dict:
    """
    Convert one source into a consistent dictionary.
    """

    # ----------------------------------------------------------
    # Dictionary
    # ----------------------------------------------------------

    if isinstance(
        source,
        dict,
    ):

        title = source.get(
            "title",
            "Unknown Source",
        )

        url = source.get(
            "url",
            "",
        )

        # Sometimes the actual URL is stored
        # under the "source" field.
        if not url:

            url = source.get(
                "source",
                "",
            )

        author = source.get(
            "author",
            "",
        )

        published_date = source.get(
            "published_date",
            "",
        )

        favicon = source.get(
            "favicon",
            "",
        )

        return {
            "title": str(title).strip()
            if title
            else "Unknown Source",

            "url": clean_url(url),

            "author": str(author).strip()
            if author
            else "",

            "published_date": str(
                published_date
            ).strip()
            if published_date
            else "",

            "favicon": str(favicon).strip()
            if favicon
            else "",
        }

    # ----------------------------------------------------------
    # String
    # ----------------------------------------------------------

    if isinstance(
        source,
        str,
    ):

        url = clean_url(source)

        return {
            "title": url or "Unknown Source",
            "url": url,
            "author": "",
            "published_date": "",
            "favicon": "",
        }

    # ----------------------------------------------------------
    # Unknown
    # ----------------------------------------------------------

    return {
        "title": str(source),
        "url": "",
        "author": "",
        "published_date": "",
        "favicon": "",
    }


# ==============================================================
# NORMALIZE COMPLETE SOURCES
# ==============================================================


def normalize_sources(sources) -> list:
    """
    Convert all possible source formats into:

    [
        {
            "title": "...",
            "url": "...",
            "author": "...",
            "published_date": "...",
            "favicon": "..."
        }
    ]
    """

    if not sources:
        return []

    # ----------------------------------------------------------
    # IMPORTANT:
    # First unwrap serialized data.
    # ----------------------------------------------------------

    sources = parse_serialized_sources(
        sources
    )

    # ----------------------------------------------------------
    # Dictionary
    # ----------------------------------------------------------

    if isinstance(
        sources,
        dict,
    ):

        # Single source object
        if (
            "title" in sources
            or "url" in sources
            or "source" in sources
        ):

            return [
                normalize_source(
                    sources
                )
            ]

        # Dictionary:
        #
        # {
        #     "Google": "https://google.com",
        #     "PubMed": "https://..."
        # }

        normalized = []

        for title, url in sources.items():

            normalized.append(
                {
                    "title": str(title),
                    "url": clean_url(url),
                    "author": "",
                    "published_date": "",
                    "favicon": "",
                }
            )

        return normalized

    # ----------------------------------------------------------
    # List
    # ----------------------------------------------------------

    if isinstance(
        sources,
        (list, tuple),
    ):

        normalized = []

        for source in sources:

            # ----------------------------------------------
            # Handle another accidental serialization layer
            # ----------------------------------------------

            if isinstance(
                source,
                str,
            ):

                parsed = parse_serialized_sources(
                    source
                )

                if isinstance(
                    parsed,
                    list,
                ):

                    for nested_source in parsed:

                        normalized.append(
                            normalize_source(
                                nested_source
                            )
                        )

                    continue

                if isinstance(
                    parsed,
                    dict,
                ):

                    normalized.append(
                        normalize_source(
                            parsed
                        )
                    )

                    continue

            # ----------------------------------------------
            # Normal source
            # ----------------------------------------------

            normalized.append(
                normalize_source(
                    source
                )
            )

        return normalized

    # ----------------------------------------------------------
    # Single string
    # ----------------------------------------------------------

    if isinstance(
        sources,
        str,
    ):

        parsed = parse_serialized_sources(
            sources
        )

        if isinstance(
            parsed,
            list,
        ):

            return [
                normalize_source(
                    source
                )
                for source in parsed
            ]

        if isinstance(
            parsed,
            dict,
        ):

            return [
                normalize_source(
                    parsed
                )
            ]

        return [
            normalize_source(
                sources
            )
        ]

    return []


# ==============================================================
# RENDER REPORT
# ==============================================================


def render_report(result: dict) -> None:
    """
    Render the generated research report.

    Responsibilities:
    - Research Report
    - Sources
    - Download
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

        report_content = result.get(
            "report",
            "No report generated.",
        )

        if report_content:

            st.markdown(
                report_content
            )

        else:

            st.info(
                "No report generated."
            )

    # ==========================================================
    # SOURCES
    # ==========================================================

    with tab2:

        raw_sources = result.get(
            "sources",
            [],
        )

        sources = normalize_sources(
            raw_sources
        )

        if not sources:

            st.info(
                "No sources available."
            )

        else:

            st.markdown(
                "## 📚 Research Sources"
            )

            st.caption(
                f"{len(sources)} sources found"
            )

            st.divider()

            # --------------------------------------------------
            # Render sources
            # --------------------------------------------------

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

                author = source.get(
                    "author",
                    "",
                )

                published_date = source.get(
                    "published_date",
                    "",
                )

                # --------------------------------------------------
                # Source card
                # --------------------------------------------------

                with st.expander(
                    f"{i}. {title}"
                ):

                    st.markdown(
                        f"**Title:** {title}"
                    )

                    if author:

                        st.markdown(
                            f"**Author:** {author}"
                        )

                    if published_date:

                        st.markdown(
                            f"**Published:** "
                            f"{published_date}"
                        )

                    if url:

                        st.markdown(
                            f"**URL:** `{url}`"
                        )

                        st.link_button(
                            "🔗 Open Source",
                            url,
                            use_container_width=True,
                        )

                    else:

                        st.caption(
                            "Source URL not available."
                        )

    # ==========================================================
    # DOWNLOAD
    # ==========================================================

    with tab3:

        st.markdown(
            "## 📥 Download Report"
        )

        st.divider()

        pdf_path = result.get(
            "pdf_path",
            "",
        )

        if (
            pdf_path
            and isinstance(
                pdf_path,
                str,
            )
            and os.path.exists(
                pdf_path
            )
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
                    file_name=(
                        "AI_Research_Report.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                )

        else:

            st.warning(
                "PDF not available."
            )