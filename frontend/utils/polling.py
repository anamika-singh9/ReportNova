import time

from frontend.api.backend import get_progress


class ProgressPoller:
    """
    Continuously polls backend progress endpoint.

    Used by Streamlit UI.
    """

    def __init__(self):

        self.running = False

    def watch(self):

        self.running = True

        while self.running:

            data = get_progress()

            if data:

                yield data

                if (
                    data["status"] == "completed"
                    and data["progress"] == 100
                ):
                    break

            time.sleep(0.20)

    def stop(self):

        self.running = False