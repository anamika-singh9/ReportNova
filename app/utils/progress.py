import threading
import time


class ProgressTracker:
    """
    Thread-safe workflow progress tracker.

    Tracks:
    - Current workflow status
    - Current running node
    - Completed nodes
    - Overall workflow percentage
    - Current node execution time
    - Total workflow execution time
    - Node history
    """

    # ==================================================
    # INITIALIZATION
    # ==================================================

    def __init__(self):

        self.lock = threading.Lock()

        self.reset()


    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        with self.lock:

            self.total_nodes = 0

            self.completed_nodes = 0

            self.workflow_start = None

            self.node_start = None

            self.current_node = ""

            self.current = {

                "workflow": "Idle",

                "node": "",

                "status": "idle",

                "progress": 0,

                "node_time": "0.00s",

                "workflow_time": "0.00s",

                "completed_nodes": 0,

                "total_nodes": 0,

            }

            self.history = []


    # ==================================================
    # WORKFLOW START
    # ==================================================

    def start_workflow(
        self,
        total_nodes: int,
    ):

        with self.lock:

            self.total_nodes = max(
                int(total_nodes),
                1,
            )

            self.completed_nodes = 0

            self.workflow_start = (
                time.perf_counter()
            )

            self.node_start = None

            self.current_node = ""

            self.history = []

            self.current = {

                "workflow": "Running",

                "node": "",

                "status": "running",

                "progress": 0,

                "node_time": "0.00s",

                "workflow_time": "0.00s",

                "completed_nodes": 0,

                "total_nodes": self.total_nodes,

            }


    # ==================================================
    # NODE START
    # ==================================================

    def start_node(
        self,
        node: str,
    ):

        with self.lock:

            self.current_node = node

            self.node_start = (
                time.perf_counter()
            )

            current_progress = (
                self._calculate_progress()
            )

            self.current.update(

                {

                    "workflow": "Running",

                    "node": node,

                    "status": "running",

                    "progress": current_progress,

                    "node_time": "0.00s",

                    "completed_nodes": (
                        self.completed_nodes
                    ),

                    "total_nodes": (
                        self.total_nodes
                    ),

                }

            )


    # ==================================================
    # NODE FINISH
    # ==================================================

    def finish_node(self):

        with self.lock:

            if not self.current_node:

                return


            # --------------------------------------------------
            # Increment completed nodes
            # --------------------------------------------------

            self.completed_nodes += 1


            # --------------------------------------------------
            # Calculate overall progress
            # --------------------------------------------------

            current_progress = (
                self._calculate_progress()
            )


            # --------------------------------------------------
            # Node execution time
            # --------------------------------------------------

            node_elapsed = 0.0

            if self.node_start:

                node_elapsed = (
                    time.perf_counter()
                    - self.node_start
                )


            # --------------------------------------------------
            # Total workflow time
            # --------------------------------------------------

            workflow_elapsed = (
                self._workflow_elapsed()
            )


            # --------------------------------------------------
            # Node history
            # --------------------------------------------------

            node_data = {

                "node": self.current_node,

                "status": "completed",

                "progress": current_progress,

                "node_time": (
                    f"{node_elapsed:.2f}s"
                ),

                "workflow_time": (
                    f"{workflow_elapsed:.2f}s"
                ),

            }


            self.history.append(
                node_data.copy()
            )


            # --------------------------------------------------
            # Update current state
            # --------------------------------------------------

            self.current.update(
                node_data
            )


            self.current[
                "completed_nodes"
            ] = self.completed_nodes

            self.current[
                "total_nodes"
            ] = self.total_nodes


            # --------------------------------------------------
            # Reset current node timer
            # --------------------------------------------------

            self.node_start = None


    # ==================================================
    # NODE FAILURE
    # ==================================================

    def fail_node(
        self,
        error: str = "",
    ):

        with self.lock:

            if not self.current_node:

                return


            # --------------------------------------------------
            # Node execution time
            # --------------------------------------------------

            node_elapsed = 0.0

            if self.node_start:

                node_elapsed = (
                    time.perf_counter()
                    - self.node_start
                )


            # --------------------------------------------------
            # Workflow time
            # --------------------------------------------------

            workflow_elapsed = (
                self._workflow_elapsed()
            )


            # --------------------------------------------------
            # Failed node data
            # --------------------------------------------------

            node_data = {

                "node": self.current_node,

                "status": "failed",

                "progress": (
                    self._calculate_progress()
                ),

                "node_time": (
                    f"{node_elapsed:.2f}s"
                ),

                "workflow_time": (
                    f"{workflow_elapsed:.2f}s"
                ),

                "error": error,

            }


            self.history.append(
                node_data.copy()
            )


            self.current.update(
                node_data
            )


            self.current[
                "completed_nodes"
            ] = self.completed_nodes

            self.current[
                "total_nodes"
            ] = self.total_nodes


            self.node_start = None


    # ==================================================
    # WORKFLOW FINISH
    # ==================================================

    def finish_workflow(self):

        with self.lock:

            workflow_elapsed = (
                self._workflow_elapsed()
            )


            self.current.update(

                {

                    "workflow": "Completed",

                    "node": "Completed",

                    "status": "completed",

                    "progress": 100,

                    "workflow_time": (
                        f"{workflow_elapsed:.2f}s"
                    ),

                    "completed_nodes": (
                        self.completed_nodes
                    ),

                    "total_nodes": (
                        self.total_nodes
                    ),

                }

            )


    # ==================================================
    # WORKFLOW FAILURE
    # ==================================================

    def fail_workflow(
        self,
        error: str = "",
    ):

        with self.lock:

            workflow_elapsed = (
                self._workflow_elapsed()
            )


            self.current.update(

                {

                    "workflow": "Failed",

                    "status": "failed",

                    "progress": (
                        self._calculate_progress()
                    ),

                    "workflow_time": (
                        f"{workflow_elapsed:.2f}s"
                    ),

                    "completed_nodes": (
                        self.completed_nodes
                    ),

                    "total_nodes": (
                        self.total_nodes
                    ),

                    "error": error,

                }

            )


    # ==================================================
    # GET CURRENT PROGRESS
    # ==================================================

    def get(self) -> dict:

        with self.lock:

            data = self.current.copy()


            # --------------------------------------------------
            # Live workflow time
            # --------------------------------------------------

            data[
                "workflow_time"
            ] = self._workflow_time_string()


            # --------------------------------------------------
            # Live current node time
            # --------------------------------------------------

            if (
                self.current.get(
                    "status"
                )
                == "running"
                and self.node_start
            ):

                node_elapsed = (
                    time.perf_counter()
                    - self.node_start
                )

                data[
                    "node_time"
                ] = (
                    f"{node_elapsed:.2f}s"
                )


            # --------------------------------------------------
            # Counts
            # --------------------------------------------------

            data[
                "completed_nodes"
            ] = self.completed_nodes

            data[
                "total_nodes"
            ] = self.total_nodes


            # --------------------------------------------------
            # Node history
            # --------------------------------------------------

            data[
                "history"
            ] = self.history.copy()


            return data


    # ==================================================
    # PRIVATE: CALCULATE OVERALL PROGRESS
    # ==================================================

    def _calculate_progress(self) -> int:

        if self.total_nodes <= 0:

            return 0


        progress = int(

            (
                self.completed_nodes
                / self.total_nodes
            )
            * 100

        )


        return min(
            max(progress, 0),
            100,
        )


    # ==================================================
    # PRIVATE: WORKFLOW ELAPSED
    # ==================================================

    def _workflow_elapsed(self) -> float:

        if not self.workflow_start:

            return 0.0


        return (
            time.perf_counter()
            - self.workflow_start
        )


    # ==================================================
    # PRIVATE: WORKFLOW TIME STRING
    # ==================================================

    def _workflow_time_string(self) -> str:

        return (
            f"{self._workflow_elapsed():.2f}s"
        )


# ==================================================
# SINGLETON
# ==================================================

progress = ProgressTracker()