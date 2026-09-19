import time

import requests

from config.constants import BACKEND_URL


# ============================================================
# COLD START CONFIG
# ============================================================
# Render free tier sleeps after ~15 min of inactivity.
# The first request after that can take 30-60s to wake up.
# These settings control how we retry during that wake-up window.

COLD_START_MAX_RETRIES = 4
COLD_START_RETRY_DELAY = 8  # seconds between retries
COLD_START_WAKE_TIMEOUT = 60  # timeout allowance for a "waking up" request


# ============================================================
# INTERNAL: RETRY WRAPPER
# ============================================================

def _request_with_retry(
    method: str,
    url: str,
    on_retry=None,
    **kwargs,
) -> requests.Response:
    """
    Wraps requests.request() with retry logic for cold starts.

    If the backend is asleep (Render free tier), the first call(s)
    may time out or fail to connect. We retry a few times with a
    short delay before giving up.

    on_retry: optional callback(attempt_number) called before each
    retry, so the UI (Streamlit) can show a "waking up" message.
    """

    last_exception = None

    for attempt in range(COLD_START_MAX_RETRIES):

        try:

            response = requests.request(
                method,
                url,
                **kwargs,
            )

            return response

        except requests.RequestException as exc:

            last_exception = exc

            is_last_attempt = (
                attempt == COLD_START_MAX_RETRIES - 1
            )

            if is_last_attempt:
                break

            if on_retry is not None:

                try:
                    on_retry(attempt + 1)
                except Exception:
                    pass

            time.sleep(COLD_START_RETRY_DELAY)

    raise ConnectionError(
        "Unable to connect to the backend server. "
        "It may be starting up — please try again in a moment."
    ) from last_exception


# ============================================================
# BACKEND STATUS
# ============================================================

def backend_online() -> bool:

    try:

        response = requests.get(
            BACKEND_URL,
            timeout=2,
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


def wake_backend(on_retry=None) -> bool:
    """
    Actively pings the backend to wake it up if it's sleeping
    (Render free tier cold start). Call this early — e.g. right
    when the app loads, or right before generate_report — so the
    backend has a head start on waking up.

    Returns True if the backend responded, False otherwise.
    """

    try:

        response = _request_with_retry(
            "GET",
            BACKEND_URL,
            on_retry=on_retry,
            timeout=COLD_START_WAKE_TIMEOUT,
        )

        return response.status_code == 200

    except ConnectionError:

        return False


# ============================================================
# AUTHENTICATION
# ============================================================

def signup(
    name: str,
    email: str,
    password: str,
    on_retry=None,
) -> dict:

    response = _request_with_retry(
        "POST",
        f"{BACKEND_URL}/auth/signup",
        on_retry=on_retry,
        json={
            "name": name,
            "email": email,
            "password": password,
        },
        timeout=COLD_START_WAKE_TIMEOUT,
    )

    if response.status_code != 201:

        try:

            detail = response.json().get(
                "detail",
                "Signup failed.",
            )

        except Exception:

            detail = (
                response.text
                or "Signup failed."
            )

        raise RuntimeError(detail)

    return response.json()


def login(
    email: str,
    password: str,
    on_retry=None,
) -> dict:

    response = _request_with_retry(
        "POST",
        f"{BACKEND_URL}/auth/login",
        on_retry=on_retry,
        json={
            "email": email,
            "password": password,
        },
        timeout=COLD_START_WAKE_TIMEOUT,
    )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Login failed.",
            )

        except Exception:

            detail = (
                response.text
                or "Login failed."
            )

        raise RuntimeError(detail)

    return response.json()


def get_current_user(
    access_token: str,
) -> dict:

    try:

        response = requests.get(
            f"{BACKEND_URL}/auth/me",
            headers={
                "Authorization":
                f"Bearer {access_token}"
            },
            timeout=10,
        )

    except requests.RequestException as exc:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from exc

    if response.status_code == 401:

        raise PermissionError(
            "Your session has expired. Please login again."
        )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to fetch user information.",
            )

        except Exception:

            detail = (
                response.text
                or "Unable to fetch user information."
            )

        raise RuntimeError(detail)

    return response.json()


# ============================================================
# LIVE WORKFLOW PROGRESS
# ============================================================

def get_progress() -> dict:

    try:

        response = requests.get(
            f"{BACKEND_URL}/progress",
            timeout=2,
        )

        if response.status_code == 200:

            data = response.json()

            return {

                "workflow": data.get(
                    "workflow",
                    "Idle",
                ),

                "node": data.get(
                    "node",
                    "",
                ),

                "status": data.get(
                    "status",
                    "idle",
                ),

                "progress": int(
                    data.get(
                        "progress",
                        0,
                    )
                ),

                "node_time": data.get(
                    "node_time",
                    "0.00s",
                ),

                "workflow_time": data.get(
                    "workflow_time",
                    "0.00s",
                ),

                "completed_nodes": data.get(
                    "completed_nodes",
                    0,
                ),

                "total_nodes": data.get(
                    "total_nodes",
                    0,
                ),

                "history": data.get(
                    "history",
                    [],
                ),

                "output": data.get(
                    "output",
                    "",
                ),

            }

    except (
        requests.RequestException,
        ValueError,
        TypeError,
    ):

        pass

    return {

        "workflow": "Idle",

        "node": "Waiting",

        "status": "idle",

        "progress": 0,

        "node_time": "0.00s",

        "workflow_time": "0.00s",

        "completed_nodes": 0,

        "total_nodes": 0,

        "history": [],

        "output": "",

    }


# ============================================================
# GENERATE REPORT
# ============================================================

def generate_report(
    topic: str,
    citation_style: str,
    access_token: str,
    uploaded_file=None,
    on_retry=None,
) -> dict:

    data = {

        "topic": topic,

        "citation_style": citation_style,

    }

    headers = {

        "Authorization":
        f"Bearer {access_token}",

    }

    if uploaded_file is not None:

        files = {

            "file": (

                uploaded_file.name,

                uploaded_file.getvalue(),

                "application/pdf",

            )

        }

        response = _request_with_retry(
            "POST",
            f"{BACKEND_URL}/generate-report",
            on_retry=on_retry,
            data=data,
            files=files,
            headers=headers,
            timeout=600,
        )

    else:

        response = _request_with_retry(
            "POST",
            f"{BACKEND_URL}/generate-report",
            on_retry=on_retry,
            data=data,
            headers=headers,
            timeout=600,
        )

    if response.status_code == 401:

        raise PermissionError(
            "Your session has expired. Please login again."
        )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Report generation failed.",
            )

        except Exception:

            detail = (
                response.text
                or "Report generation failed."
            )

        raise RuntimeError(detail)

    return response.json()


# ============================================================
# REPORTS
# ============================================================

def get_reports(
    access_token: str,
) -> list:

    try:

        response = requests.get(

            f"{BACKEND_URL}/reports/",

            headers={
                "Authorization":
                f"Bearer {access_token}"
            },

            timeout=10,

        )

    except requests.RequestException as exc:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from exc

    if response.status_code == 401:

        raise PermissionError(
            "Your session has expired. Please login again."
        )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to fetch reports.",
            )

        except Exception:

            detail = (
                response.text
                or "Unable to fetch reports."
            )

        raise RuntimeError(detail)

    return response.json()


# ============================================================
# GET SINGLE REPORT
# ============================================================

def get_report(
    report_id: int,
    access_token: str,
) -> dict:

    try:

        response = requests.get(

            f"{BACKEND_URL}/reports/{report_id}",

            headers={
                "Authorization":
                f"Bearer {access_token}"
            },

            timeout=10,

        )

    except requests.RequestException as exc:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from exc

    if response.status_code == 401:

        raise PermissionError(
            "Your session has expired. Please login again."
        )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to fetch report.",
            )

        except Exception:

            detail = (
                response.text
                or "Unable to fetch report."
            )

        raise RuntimeError(detail)

    return response.json()


# ============================================================
# DOWNLOAD REPORT PDF
# ============================================================

def download_report_pdf(
    report_id: int,
    access_token: str,
) -> bytes:

    try:

        response = requests.get(

            f"{BACKEND_URL}/reports/{report_id}/download",

            headers={
                "Authorization":
                f"Bearer {access_token}"
            },

            timeout=30,

        )

    except requests.RequestException as exc:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from exc

    if response.status_code == 401:

        raise PermissionError(
            "Your session has expired. Please login again."
        )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to download PDF.",
            )

        except Exception:

            detail = (
                response.text
                or "Unable to download PDF."
            )

        raise RuntimeError(detail)

    return response.content


# ============================================================
# DELETE REPORT
# ============================================================

def delete_report(
    report_id: int,
    access_token: str,
) -> dict:

    try:

        response = requests.delete(

            f"{BACKEND_URL}/reports/{report_id}",

            headers={
                "Authorization":
                f"Bearer {access_token}"
            },

            timeout=10,

        )

    except requests.RequestException as exc:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from exc

    if response.status_code == 401:

        raise PermissionError(
            "Your session has expired. Please login again."
        )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to delete report.",
            )

        except Exception:

            detail = (
                response.text
                or "Unable to delete report."
            )

        raise RuntimeError(detail)

    return response.json()