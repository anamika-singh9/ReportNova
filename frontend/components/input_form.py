import streamlit as st


def render_input_form():
    """
    Render research input form.
    """

    with st.container(border=True):

        st.markdown("## 🔬 Research Configuration")

        st.caption(
            "Provide your research topic and optional documents."
        )

        topic = st.text_input(
            "Research Topic",
            placeholder="Generative AI in Healthcare",
        )

        uploaded_file = st.file_uploader(
            "Upload PDF (Optional)",
            type=["pdf"],
        )

        if uploaded_file:

            st.success(
                f"Uploaded : {uploaded_file.name}"
            )

        citation_style = st.selectbox(
            "Citation Style",
            [
                "APA",
                "IEEE",
            ],
        )

        generate = st.button(
            "🚀 Generate Research Report",
            use_container_width=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        progress_placeholder = st.empty()

        timeline_placeholder = st.empty()

    return (
        topic,
        uploaded_file,
        citation_style,
        generate,
        progress_placeholder,
        timeline_placeholder,
    )