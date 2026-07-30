class ReportGenerationError(Exception):
    """
    Raised when report generation fails.
    """
    pass


class ResearchError(Exception):
    """
    Raised when research fails.
    """
    pass


class PDFGenerationError(Exception):
    """
    Raised when PDF generation fails.
    """
    pass


class CitationError(Exception):
    """
    Raised when citation generation fails.
    """
    pass


class ModelError(Exception):
    """
    Raised when the LLM fails.
    """
    pass