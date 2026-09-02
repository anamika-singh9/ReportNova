import ast
import json
import os
import re

import streamlit as st

from frontend.api.backend import (
    download_report_pdf,
    get_report,
)


# ============================================================
# SOURCE NORMALIZATION
# ============================================================

def clean_url(
    url,
) -> str:

    if url is None:

        return ""


    value = str(
        url
    ).strip()


    # Markdown URL:
    # [Google](https://google.com)

    markdown_match = re.match(

        r"^\[[^\]]*\]\((https?://[^)]+)\)$",

        value,

        flags=re.IGNORECASE,

    )


    if markdown_match:

        value = (
            markdown_match.group(1)
            .strip()
        )


    # Remove wrappers

    value = value.strip(
        "<>\"'"
    )


    # Remove accidental punctuation

    value = value.rstrip(
        ".,;)"
    )


    if value.lower().startswith(
        (
            "http://",
            "https://",
        )
    ):

        return value


    return ""


# ============================================================
# PARSE SERIALIZED SOURCES
# ============================================================

def parse_serialized_sources(
    sources,
):

    if sources is None:

        return []


    if isinstance(
        sources,
        (
            list,
            dict,
        ),
    ):

        return sources


    if not isinstance(
        sources,
        str,
    ):

        return []


    value = sources.strip()


    if not value:

        return []


    # ========================================================
    # JSON
    # ========================================================

    try:

        parsed = json.loads(
            value
        )


        if parsed != value:

            return parsed


    except (
        json.JSONDecodeError,
        TypeError,
    ):

        pass


    # ========================================================
    # PYTHON-LITERAL FORMAT
    # ========================================================

    try:

        parsed = ast.literal_eval(
            value
        )


        if parsed != value:

            return parsed


    except (
        ValueError,
        SyntaxError,
        TypeError,
    ):

        pass


    return value


# ============================================================
# NORMALIZE ONE SOURCE
# ============================================================

def normalize_source(
    source,
):

    if isinstance(
        source,
        dict,
    ):

        # Handle nested source object

        if isinstance(
            source.get("source"),
            dict,
        ):

            nested = dict(
                source["source"]
            )


            nested.update({

                key: value

                for key, value
                in source.items()

                if key != "source"

            })


            source = nested


        title = (

            source.get("title")

            or source.get("name")

            or source.get("headline")

            or "Untitled Source"

        )


        author = (

            source.get("author")

            or source.get("organization")

            or source.get("domain")

            or source.get("source")

            or "Unknown"

        )


        published = (

            source.get("published_date")

            or source.get("published")

            or source.get("date")

            or "n.d."

        )


        url = clean_url(

            source.get("url")

            or source.get("link")

            or source.get("source_url")

            or source.get("href")

            or ""

        )


        return {

            "title": str(title),

            "author": str(author),

            "published": str(
                published
            ),

            "url": url,

        }


    # ========================================================
    # SOURCE STORED AS STRING
    # ========================================================

    if isinstance(
        source,
        str,
    ):

        value = source.strip()


        url_match = re.search(

            r"https?://[^\s<>\"')\]]+",

            value,

            re.IGNORECASE,

        )


        url = (

            clean_url(
                url_match.group(0)
            )

            if url_match

            else ""

        )


        title = value


        if url and value != url:

            title = (

                value
                .replace(
                    url,
                    "",
                )
                .strip(
                    " -|:"
                )

                or "Source"

            )


        return {

            "title":
                title or "Source",

            "author":
                "Unknown",

            "published":
                "n.d.",

            "url":
                url,

        }


    return {

        "title":
            "Untitled Source",

        "author":
            "Unknown",

        "published":
            "n.d.",

        "url":
            "",

    }


# ============================================================
# NORMALIZE SOURCES
# ============================================================

def normalize_sources(
    sources,
) -> list:

    parsed = parse_serialized_sources(
        sources
    )


    # ========================================================
    # DICTIONARY WRAPPER
    # ========================================================

    if isinstance(
        parsed,
        dict,
    ):

        for key in (

            "sources",

            "results",

            "references",

            "items",

            "data",

        ):

            if key in parsed:

                parsed = parsed[key]

                break

        else:

            parsed = [
                parsed
            ]


    # ========================================================
    # PLAIN STRING
    # ========================================================

    if isinstance(
        parsed,
        str,
    ):

        urls = re.findall(

            r"https?://[^\s<>\"')\]]+",

            parsed,

            flags=re.IGNORECASE,

        )


        return [

            normalize_source(
                url
            )

            for url in urls

        ]


    if not isinstance(
        parsed,
        list,
    ):

        return []


    normalized = []


    # ========================================================
    # NORMALIZE EACH SOURCE
    # ========================================================

    for item in parsed:

        if isinstance(
            item,
            str,
        ):

            nested = parse_serialized_sources(
                item
            )


            if (
                isinstance(
                    nested,
                    (
                        list,
                        dict,
                    ),
                )
                and nested != item
            ):

                normalized.extend(
                    normalize_sources(
                        nested
                    )
                )

                continue


        source = normalize_source(
            item
        )


        if (
            source["url"]
            or
            source["title"]
            not in {
                "Untitled Source",
                "Source",
            }
        ):

            normalized.append(
                source
            )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique = []

    seen = set()


    for source in normalized:

        key = (

            source["url"]

            or (

                source["title"],

                source["author"],

                source["published"],

            )

        )


        if key in seen:

            continue


        seen.add(
            key
        )


        unique.append(
            source
        )


    return unique


# ============================================================
# LOCAL PDF
# ============================================================

def _local_pdf_bytes(
    pdf_path: str,
):

    if not pdf_path:

        return None


    try:

        if os.path.exists(
            pdf_path
        ):

            with open(
                pdf_path,
                "rb",
            ) as pdf_file:

                return pdf_file.read()


    except OSError:

        pass


    return None


# ============================================================
# PDF DOWNLOAD
# ============================================================

def _get_pdf_bytes(
    result: dict,
):

    report_id = result.get(
        "report_id",
        result.get("id"),
    )


    access_token = (
        st.session_state.get(
            "access_token"
        )
    )


    # ========================================================
    # SAVED REPORT
    # ========================================================

    if (
        report_id is not None
        and access_token
    ):

        try:

            data = download_report_pdf(

                report_id=int(
                    report_id
                ),

                access_token=access_token,

            )


            if data:

                return data


        except Exception:

            pass


    # ========================================================
    # LOCAL FALLBACK
    # ========================================================

    return _local_pdf_bytes(

        result.get(
            "pdf_path",
            "",
        )

    )


# ============================================================
# RENDER REPORT
# ============================================================

def render_report(
    result: dict,
):

    if not isinstance(
        result,
        dict,
    ):

        st.error(
            "No valid report is available."
        )

        return


    report_content = (

        result.get(
            "report_content"
        )

        or result.get(
            "report"
        )

        or ""

    )


    sources = normalize_sources(

        result.get(
            "sources",
            [],
        )

    )


    # ========================================================
    # TABS
    # ========================================================

    tab_report, tab_sources, tab_download = st.tabs(

        [

            "📄 Research Report",

            "🔗 Sources",

            "⬇️ Download",

        ]

    )


    # ========================================================
    # REPORT
    # ========================================================

    with tab_report:

        if report_content:

            st.markdown(
                report_content
            )

        else:

            st.info(
                "No report content is available."
            )


    # ========================================================
    # SOURCES
    # ========================================================

    with tab_sources:

        st.subheader(
            "Research Sources"
        )


        if not sources:

            st.info(
                "No source metadata is available "
                "for this report."
            )


        else:

            st.caption(

                f"{len(sources)} "
                "source(s) used for this report"

            )


            for index, source in enumerate(
                sources,
                start=1,
            ):

                st.markdown(

                    f"### {index}. "
                    f"{source['title']}"

                )


                st.write(

                    "**Author / Organization:** "
                    f"{source['author']}"

                )


                st.write(

                    "**Published:** "
                    f"{source['published']}"

                )


                if source["url"]:

                    st.code(
                        source["url"],
                        language=None,
                    )


                    st.link_button(

                        "🔗 Open Source",

                        source["url"],

                        width="content",

                    )

                else:

                    st.caption(
                        "Source URL is not available."
                    )


                if index < len(
                    sources
                ):

                    st.divider()


    # ========================================================
    # DOWNLOAD
    # ========================================================

    with tab_download:

        st.subheader(
            "Download Report"
        )


        pdf_bytes = _get_pdf_bytes(
            result
        )


        if pdf_bytes:

            report_id = result.get(

                "report_id",

                result.get("id"),

            )


            suffix = (

                f"_{report_id}"

                if report_id is not None

                else ""

            )


            st.download_button(

                label="⬇️ Download PDF",

                data=pdf_bytes,

                file_name=(
                    f"ReportNova_Report"
                    f"{suffix}.pdf"
                ),

                mime="application/pdf",

                width="stretch",

            )


        else:

            st.warning(

                "The PDF file is not available. "
                "The report itself is still available above."

            )


# ============================================================
# SAVED REPORT PAGE
# ============================================================

def render_report_page():

    report_id = (
        st.session_state.get(
            "selected_report_id"
        )
    )


    result = (
        st.session_state.get(
            "result"
        )
    )


    # ========================================================
    # FETCH REPORT IF NECESSARY
    # ========================================================

    if report_id is not None:

        current_id = (

            None

            if not isinstance(
                result,
                dict,
            )

            else result.get(
                "report_id",
                result.get("id"),
            )

        )


        if current_id != report_id:

            try:

                fetched = get_report(

                    report_id=int(
                        report_id
                    ),

                    access_token=(
                        st.session_state.access_token
                    ),

                )


                if not isinstance(
                    fetched,
                    dict,
                ):

                    raise RuntimeError(
                        "Invalid report received from backend."
                    )


                from frontend.services.session import (
                    save_result,
                )


                save_result(
                    fetched
                )


                result = (
                    st.session_state.get(
                        "result"
                    )
                )


            except PermissionError:

                st.error(
                    "Your session has expired. "
                    "Please login again."
                )

                return


            except Exception as exc:

                st.error(
                    f"Unable to load this report: {exc}"
                )

                return


    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title(
        "📄 Saved Report"
    )


    if isinstance(
        result,
        dict,
    ):

        topic = result.get(
            "topic",
            "Untitled Report",
        )


        citation_style = result.get(
            "citation_style",
            "",
        )


        st.subheader(
            str(topic)
        )


        if citation_style:

            st.caption(
                f"Citation style: {citation_style}"
            )


        if st.button(
            "← Back to History",
            width="content",
        ):

            st.session_state.current_page = (
                "history"
            )

            st.session_state.selected_report_id = (
                None
            )

            st.session_state.result = (
                None
            )

            st.rerun()


        st.markdown("---")


        render_report(
            result
        )


    else:

        st.info(
            "Select a report from History to view it."
        )