import os

# ----------------------------
# Base Directory
# ----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# ----------------------------
# Data Directories
# ----------------------------

DATA_DIR = os.path.join(BASE_DIR, "data")

UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

REPORT_DIR = os.path.join(BASE_DIR, "app", "output")

LOG_DIR = os.path.join(BASE_DIR, "app", "logs")

VECTOR_DB_DIR = os.path.join(DATA_DIR, "vector_db")

CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

# ----------------------------
# Default Files
# ----------------------------

DEFAULT_REPORT_NAME = "research_report.pdf"

# ----------------------------
# API
# ----------------------------

BACKEND_URL = "http://127.0.0.1:8000"