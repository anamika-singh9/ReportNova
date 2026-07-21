import streamlit as st
import requests

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="AI Research Lab",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Title
# -------------------------------

st.title("🤖 AI Research Report Generator")

st.write("Generate AI-powered research reports using Agentic AI.")

# -------------------------------
# Topic Input
# -------------------------------

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Artificial Intelligence"
)

# -------------------------------
# Generate Button
# -------------------------------

if st.button("Generate Report", use_container_width=True):

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
    else:

        with st.spinner("Generating Report..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/generate-report",
                    json={"topic": topic},
                    timeout=300
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("Report Generated Successfully!")

                    st.markdown(result["report"])

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(str(e))