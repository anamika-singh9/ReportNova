import time

from frontend.api.backend import get_progress


class ProgressService:
    """
    Handles live workflow progress polling.

    Responsibilities:
    - Poll backend progress endpoint.
    - Return latest workflow status.
    - Wait between requests to avoid excessive API calls.
    """

    def __init__(
        self,
        interval: float = 0.2,
    ):

        self.interval = interval

    def get(self) -> dict:
        """
        Get latest workflow progress.

        Returns:
            dict
        """

        return get_progress()

    def stream(self):
        """
        Generator that continuously yields progress updates
        until workflow reaches 100%.
        """

        while True:

            data = self.get()

            yield data

            if data.get("progress", 0) >= 100:
                break

            time.sleep(self.interval)