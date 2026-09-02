import streamlit as st


class TimelineUI:
    """
    Detailed live workflow timeline.

    Responsibilities:
    - Show executed agents.
    - Show currently running agent.
    - Show execution time.
    - Show workflow progress.
    - Show expandable agent output.
    - Show remaining agents.

    This component only handles UI rendering.
    """


    # ==================================================
    # INITIALIZATION
    # ==================================================

    def __init__(
        self,
        placeholder=None,
    ):

        if placeholder is not None:

            self.container = placeholder

        else:

            self.container = st.container()


        self.nodes = {}


        # Expected LangGraph execution order.
        #
        # Conditional routing may stop the workflow,
        # therefore these are only displayed as
        # possible/future nodes.

        self.expected_nodes = [
            "Planner",
            "Research",
            "Fact Checker",
            "Writer",
            "Citation",
            "Reviewer",
            "PDF Generator",
        ]


    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        data: dict,
    ):
        """
        Update timeline using live backend progress.
        """

        if not data:

            return


        node = data.get(
            "node",
            "",
        )

        status = data.get(
            "status",
            "idle",
        )

        progress = int(
            data.get(
                "progress",
                0,
            )
        )

        node_time = data.get(
            "node_time",
            "0.00s",
        )

        workflow_time = data.get(
            "workflow_time",
            "0.00s",
        )

        history = data.get(
            "history",
            [],
        )


        # --------------------------------------------------
        # Rebuild node state from backend history
        # --------------------------------------------------

        for item in history:

            item_node = item.get(
                "node",
                "",
            )

            if not item_node:

                continue


            self.nodes[item_node] = {

                "status": item.get(
                    "status",
                    "completed",
                ),

                "node_time": item.get(
                    "node_time",
                    "0.00s",
                ),

                "output": item.get(
                    "output",
                    "",
                ),
            }


        # --------------------------------------------------
        # Current running node
        # --------------------------------------------------

        if (
            node
            and node != "Completed"
            and status == "running"
        ):

            self.nodes[node] = {

                "status": "running",

                "node_time": node_time,

                "output": data.get(
                    "output",
                    "",
                ),
            }


        # --------------------------------------------------
        # Render
        # --------------------------------------------------

        self.render(
            progress=progress,
            workflow_time=workflow_time,
        )


    # ==================================================
    # STATUS ICON
    # ==================================================

    @staticmethod
    def _get_icon(
        status: str,
    ) -> str:

        if status == "completed":

            return "✅"

        if status == "running":

            return "🔄"

        if status == "failed":

            return "❌"

        return "○"


    # ==================================================
    # RENDER
    # ==================================================

    def render(
        self,
        progress: int = 0,
        workflow_time: str = "0.00s",
    ):
        """
        Render the complete agent timeline.
        """

        self.container.empty()


        with self.container:

            st.markdown(
                "## 🤖 Agent Timeline"
            )


            # --------------------------------------------------
            # Overall information
            # --------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.caption(
                    "Workflow Progress"
                )

                st.write(
                    f"**{progress}%**"
                )

            with col2:

                st.caption(
                    "Total Execution"
                )

                st.write(
                    f"**{workflow_time}**"
                )


            st.progress(
                progress / 100
            )


            st.markdown(
                "---"
            )


            # --------------------------------------------------
            # Agent timeline
            # --------------------------------------------------

            for index, node in enumerate(
                self.expected_nodes
            ):

                info = self.nodes.get(
                    node,
                    {
                        "status": "pending",
                        "node_time": "0.00s",
                        "output": "",
                    },
                )


                status = info.get(
                    "status",
                    "pending",
                )

                node_time = info.get(
                    "node_time",
                    "0.00s",
                )

                output = info.get(
                    "output",
                    "",
                )


                icon = self._get_icon(
                    status
                )


                # --------------------------------------------------
                # Completed / running node
                # --------------------------------------------------

                if status in (
                    "completed",
                    "running",
                    "failed",
                ):

                    with st.expander(
                        f"{icon} {node}  •  {node_time}",
                        expanded=(
                            status
                            == "running"
                        ),
                    ):

                        if status == "running":

                            st.info(
                                "Agent is currently running..."
                            )

                        elif status == "completed":

                            st.success(
                                f"Completed in {node_time}"
                            )

                        elif status == "failed":

                            st.error(
                                f"Agent failed after "
                                f"{node_time}"
                            )


                        # ------------------------------------------
                        # Output
                        # ------------------------------------------

                        if output:

                            st.caption(
                                "Agent Output"
                            )

                            st.code(
                                output[:800]
                            )


                # --------------------------------------------------
                # Pending node
                # --------------------------------------------------

                else:

                    st.markdown(
                        f"○ **{node}**  "
                        f"<span style='opacity:0.55'>Pending</span>",
                        unsafe_allow_html=True,
                    )


                # --------------------------------------------------
                # Connector
                # --------------------------------------------------

                if (
                    index
                    < len(
                        self.expected_nodes
                    ) - 1
                ):

                    st.markdown(
                        "<div style='"
                        "margin-left:10px;"
                        "height:10px;"
                        "border-left:2px solid "
                        "rgba(255,255,255,0.15);"
                        "'></div>",
                        unsafe_allow_html=True,
                    )