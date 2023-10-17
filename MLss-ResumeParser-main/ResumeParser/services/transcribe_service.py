

import requests
from typing import Dict
from ResumeParser.config import settings


class TranscribeService:
    """Transcribe Service for files."""

    def __init__(
        self
    ) -> None:
        pass

    def __call__(self, file_name: str) -> Dict[str, str]:

        url = settings.transcriber_endpoint
        with open(file_name, "rb") as f:
            files = {"file": f}
            data = {"timestamps": "s", "is_digital": None}
            response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            extracted_text_combined = result['transcriberOutput']["fileText"]
        else:
            raise "Transcriber raised an error."
        return {"extracted_text": extracted_text_combined}
