
from typing import Dict


class PreProcessingService:
    """Pre-Processing Service for resume files."""

    def __init__(self) -> None:
        """Initialize the PreProcessingService."""

    def __call__(self, doc_path) -> Dict[str, str]:
        return {"ip_file": doc_path}
