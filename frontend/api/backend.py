import requests

from config.constants import BACKEND_URL


# ==================================================
# BACKEND STATUS
# ==================================================

def backend_online() -> bool:
    """
    Check whether the backend server is running.
    """

    try:

        response = requests.get(
            BACKEND_URL,
            timeout=2,
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


# ==================================================
# AUTHENTICATION
# ==================================================

def signup(
    name: str,
    email: str,
    password: str,
) -> dict:

    url = f"{BACKEND_URL}/auth/signup"

    data = {
        "name": name,
        "email": email,
        "password": password,
    }

    try:

        response = requests.post(
            url,
            json=data,
            timeout=10,
        )

    except requests.RequestException as e:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from e

    if response.status_code != 201:

        raise RuntimeError(
            response.json().get(
                "detail",
                "Signup failed.",
            )
        )

    return response.json()


def login(
    email: str,
    password: str,
) -> dict:

    url = f"{BACKEND_URL}/auth/login"

    data = {
        "email": email,
        "password": password,
    }

    try:

        response = requests.post(
            url,
            json=data,
            timeout=10,
        )

    except requests.RequestException as e:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from e

    if response.status_code != 200:

        raise RuntimeError(
            response.json().get(
                "detail",
                "Login failed.",
            )
        )

    return response.json()


# ==================================================
# PROGRESS
# ==================================================

def get_progress() -> dict:
    """
    Fetch live workflow progress from the backend.
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


# ==================================================
# GENERATE REPORT
# ==================================================

def generate_report(
    topic: str,
    citation_style: str,
    access_token: str,
    uploaded_file=None,
) -> dict:
    """
    Send an authenticated report generation request.
    """

    url = f"{BACKEND_URL}/generate-report"

    data = {
        "topic": topic,
        "citation_style": citation_style,
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
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
                headers=headers,
                timeout=600,
            )

        else:

            response = requests.post(
                url,
                data=data,
                headers=headers,
                timeout=600,
            )

    except requests.RequestException as e:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from e

    if response.status_code == 401:

        raise PermissionError(
            "Your session has expired. Please login again."
        )

    if response.status_code != 200:

        raise RuntimeError(
            response.json().get(
                "detail",
                "Report generation failed.",
            )
        )

    return response.json()


# ==================================================
# REPORTS
# ==================================================

def get_reports(
    access_token: str,
) -> list:
    """
    Get all reports of the currently logged-in user.
    """

    url = f"{BACKEND_URL}/reports/"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

    except requests.RequestException as e:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from e

    if response.status_code == 401:

        raise PermissionError(
            "Your session has expired. Please login again."
        )

    if response.status_code != 200:

        raise RuntimeError(
            response.json().get(
                "detail",
                "Unable to fetch reports.",
            )
        )

    return response.json()

# ==========================================
# GET SINGLE REPORT
# ==========================================

def get_report(
    report_id: int,
    access_token: str,
) -> dict:

    url = f"{BACKEND_URL}/reports/{report_id}"

    headers = {
        "Authorization": (
            f"Bearer {access_token}"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10,
    )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to fetch report."
            )

        except Exception:

            detail = response.text

        raise RuntimeError(detail)

    return response.json()


# ==========================================
# DELETE REPORT
# ==========================================

def delete_report(
    report_id: int,
    access_token: str,
) -> dict:

    url = f"{BACKEND_URL}/reports/{report_id}"

    headers = {
        "Authorization": (
            f"Bearer {access_token}"
        )
    }

    response = requests.delete(
        url,
        headers=headers,
        timeout=10,
    )

    if response.status_code != 200:

        try:

            detail = response.json().get(
                "detail",
                "Unable to delete report."
            )

        except Exception:

            detail = response.text

        raise RuntimeError(detail)

    return response.json()


# ==================================================
# GET CURRENT USER
# ==================================================

def get_current_user(
    access_token: str,
) -> dict:
    """
    Get details of the currently authenticated user.
    """

    url = f"{BACKEND_URL}/auth/me"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

    except requests.RequestException as e:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from e

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

            detail = response.text

        raise RuntimeError(detail)

    return response.json()