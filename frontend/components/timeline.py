import streamlit as st


class TimelineUI:
    """
    Live workflow timeline.

    Shows:
    - Running node
    - Completed nodes
    - Future nodes
    - Expandable output
    """

    def __init__(self):

        self.container = st.container()

        self.nodes = {}

    def update(self, data):

        node = data.get("node")

        status = data.get("status")

        output = data.get("output", "")

        if node not in self.nodes:

            self.nodes[node] = {
                "status": status,
                "output": output,
            }

        else:

            self.nodes[node]["status"] = status

            if output:

                self.nodes[node]["output"] = output

        self.render()

    def render(self):

        self.container.empty()

        with self.container:

            st.markdown("## 🤖 Agent Timeline")

            for node, info in self.nodes.items():

                status = info["status"]

                if status == "completed":

                    icon = "✅"

                elif status == "running":

                    icon = "🔄"

                elif status == "failed":

                    icon = "❌"

                else:

                    icon = "⚪"

                with st.expander(
                    f"{icon} {node}",
                    expanded=status == "running",
                ):

                    st.write(f"Status : **{status}**")

                    if info["output"]:

                        preview = info["output"][:800]

                        st.code(preview)


