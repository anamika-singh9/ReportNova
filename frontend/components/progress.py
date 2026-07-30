import streamlit as st


class ProgressUI:
    """
    Professional live workflow progress component.
    """

    def __init__(self):

        self.container = st.container()

        with self.container:

            st.markdown("## 🚀 Workflow Progress")

            self.bar = st.progress(0)

            self.percent = st.empty()

            self.current_agent = st.empty()

            self.status = st.empty()

            self.elapsed = st.empty()

            st.divider()

    def update(self, data):

        progress = int(data.get("progress", 0))

        node = data.get("node", "-")

        status = data.get("status", "-")

        elapsed = data.get("time", "0.00s")

        self.bar.progress(progress)

        self.percent.metric(
            "Progress",
            f"{progress}%",
        )

        self.current_agent.info(
            f"🤖 Current Agent : {node}"
        )

        if status == "running":

            self.status.warning("Running...")

        elif status == "completed":

            self.status.success("Completed")

        elif status == "failed":

            self.status.error("Failed")

        else:

            self.status.info(status)

        self.elapsed.caption(
            f"Elapsed : {elapsed}"
        )