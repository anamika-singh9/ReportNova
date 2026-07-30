import requests

from config.constants import BACKEND_URL


def get_progress():

    try:

        response = requests.get(
            f"{BACKEND_URL}/progress",
            timeout=2,
        )

        if response.status_code == 200:

            return response.json()

    except Exception:

        pass

    return None