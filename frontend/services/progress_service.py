import time

from frontend.api.backend import get_progress


class ProgressService:
    """
    Service responsible for retrieving backend workflow progress.

    The service does NOT modify Streamlit session state.
    """

    def __init__(
        self,
        interval: float = 0.5,
    ):
        self.interval = interval

    # ========================================================
    # GET CURRENT PROGRESS
    # ========================================================

    def get(self) -> dict:

        return get_progress()

    # ========================================================
    # STREAM
    # ========================================================

    def stream(self):

        while True:

            data = self.get()

            yield data

            status = data.get(
                "status",
                "idle",
            )

            if status in (
                "completed",
                "failed",
            ):

                break

            time.sleep(
                self.interval
            )

    # ========================================================
    # WAIT
    # ========================================================

    def wait_until_finished(self):

        while True:

            data = self.get()

            status = data.get(
                "status",
                "idle",
            )

            if status in (
                "completed",
                "failed",
            ):

                return data

            time.sleep(
                self.interval
            )