import requests

from config.constants import BACKEND_URL


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


# ============================================================
# AUTHENTICATION
# ============================================================

def signup(
    name: str,
    email: str,
    password: str,
) -> dict:

    try:

        response = requests.post(
            f"{BACKEND_URL}/auth/signup",
            json={
                "name": name,
                "email": email,
                "password": password,
            },
            timeout=10,
        )

    except requests.RequestException as exc:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from exc


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
) -> dict:

    try:

        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json={
                "email": email,
                "password": password,
            },
            timeout=10,
        )

    except requests.RequestException as exc:

        raise ConnectionError(
            "Unable to connect to the backend server."
        ) from exc


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
) -> dict:

    data = {

        "topic": topic,

        "citation_style": citation_style,

    }


    headers = {

        "Authorization":
        f"Bearer {access_token}",

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

                f"{BACKEND_URL}/generate-report",

                data=data,

                files=files,

                headers=headers,

                timeout=600,

            )

        else:

            response = requests.post(

                f"{BACKEND_URL}/generate-report",

                data=data,

                headers=headers,

                timeout=600,

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