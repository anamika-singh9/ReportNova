import threading
import time


class ProgressTracker:
    """
    Production-ready workflow progress tracker.

    Tracks:
    - Current running node
    - Completed nodes
    - Dynamic percentage
    - Node execution time
    - Total workflow time
    """

    def __init__(self):

        self.lock = threading.Lock()

        self.reset()

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Workflow Start
    # --------------------------------------------------

    def start_workflow(self, total_nodes: int):

        with self.lock:

            self.total_nodes = total_nodes
            self.completed_nodes = 0

            self.workflow_start = time.perf_counter()

            self.current.update(
                {
                    "workflow": "Running",
                    "status": "running",
                    "progress": 0,
                    "completed_nodes": 0,
                    "total_nodes": total_nodes,
                }
            )

    # --------------------------------------------------
    # Node Start
    # --------------------------------------------------

    def start_node(self, node: str):

        with self.lock:

            self.current_node = node

            self.node_start = time.perf_counter()

            progress = int(
                (self.completed_nodes / self.total_nodes) * 100
            )

            self.current.update(
                {
                    "node": node,
                    "status": "running",
                    "progress": progress,
                }
            )

    # --------------------------------------------------
    # Node Finish
    # --------------------------------------------------

    def finish_node(self):

        with self.lock:

            self.completed_nodes += 1

            progress = int(
                (self.completed_nodes / self.total_nodes) * 100
            )

            node_elapsed = (
                time.perf_counter()
                - self.node_start
            )

            workflow_elapsed = (
                time.perf_counter()
                - self.workflow_start
            )

            node_data = {
                "node": self.current_node,
                "status": "completed",
                "progress": progress,
                "node_time": f"{node_elapsed:.2f}s",
                "workflow_time": f"{workflow_elapsed:.2f}s",
            }

            self.history.append(node_data)

            self.current.update(node_data)

            self.current["completed_nodes"] = self.completed_nodes

    # --------------------------------------------------
    # Workflow Finish
    # --------------------------------------------------

    def finish_workflow(self):

        with self.lock:

            workflow_elapsed = (
                time.perf_counter()
                - self.workflow_start
            )

            self.current.update(
                {
                    "workflow": "Completed",
                    "node": "Completed",
                    "status": "completed",
                    "progress": 100,
                    "workflow_time": f"{workflow_elapsed:.2f}s",
                }
            )

    # --------------------------------------------------
    # API Response
    # --------------------------------------------------

    def get(self):

        with self.lock:

            workflow_time = "0.00s"

            if self.workflow_start:

                workflow_time = (
                    f"{time.perf_counter() - self.workflow_start:.2f}s"
                )

            data = self.current.copy()

            data["workflow_time"] = workflow_time

            data["history"] = self.history.copy()

            return data


# Singleton instance
progress = ProgressTracker()