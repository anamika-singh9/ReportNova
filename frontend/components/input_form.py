import streamlit as st


def render_input_form():
    """
    Render research input form.
    """

    with st.container(
        border=True
    ):

        st.markdown(
            "## 🔬 Research Configuration"
        )

        st.caption(
            "Provide your research topic "
            "and optional documents."
        )

        topic = st.text_input(
            "Research Topic",
            placeholder=(
                "Generative AI in Healthcare"
            ),
        )

        uploaded_file = st.file_uploader(
            "Upload PDF (Optional)",
            type=["pdf"],
        )

        if uploaded_file:

            st.success(
                f"Uploaded: "
                f"{uploaded_file.name}"
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
            width="stretch",
        )

    return (
        topic,
        uploaded_file,
        citation_style,
        generate,
    )


