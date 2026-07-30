import requests

from config.constants import BACKEND_URL


def backend_online() -> bool:
    """
    Check whether the backend server is running.

    Returns:
        bool:
            True  -> Backend is reachable.
            False -> Backend is offline.
    """

    try:

        response = requests.get(
            BACKEND_URL,
            timeout=2,
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


def get_progress() -> dict:
    """
    Fetch live workflow progress from the backend.

    Returns:
        dict containing current workflow state.
    """

    try:

        response = requests.get(
            f"{BACKEND_URL}/progress",
            timeout=2,
        )

        if response.status_code == 200:

            return response.json()

    except requests.RequestException:
        pass

    return {
        "node": "Waiting",
        "status": "idle",
        "progress": 0,
        "time": "0.00s",
        "output": "",
    }


def generate_report(
    topic: str,
    citation_style: str,
    uploaded_file=None,
) -> dict:
    """
    Send a report generation request to the backend.

    Args:
        topic:
            Research topic.

        citation_style:
            APA / IEEE.

        uploaded_file:
            Optional PDF uploaded by the user.

    Returns:
        Backend JSON response.

    Raises:
        ConnectionError
        RuntimeError
    """

    url = f"{BACKEND_URL}/generate-report"

    data = {
        "topic": topic,
        "citation_style": citation_style,
    }

    try:

        if uploaded_file is not None:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            }

            response = requests.post(
                url,
                data=data,
                files=files,
                timeout=600,
            )

        else:

            response = requests.post(
                url,
                data=data,
                timeout=600,
            )

    except requests.RequestException as e:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from e

    if response.status_code != 200:

        raise RuntimeError(
            response.text
        )

    return response.json()