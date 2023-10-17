"""Configuration module of the ResumeParser."""

from pydantic.dataclasses import dataclass
from ResumeParser import __version__


@dataclass
class Settings:
    """Configuration settings for the ResumeParser API."""

    # General configuration
    project_name: str
    version: str
    description: str
    api_prefix: str
    debug: bool
    storage_dir: str
    log_file: str
    # Models configuration
    transcriber_endpoint: str
    openai_key: str
    # Service type configuration
    service_type: str

    # Endpoints configuration
    resume_parser_endpoint: bool
    front_end_point: str
    # API authentication configuration
    username: str
    password: str
    openssl_key: str
    openssl_algorithm: str
    access_token_expire_minutes: int


settings = Settings(
    # General configuration
    project_name="ResumeParser",
    version=__version__,
    description="ResumeParser FastAPI server.",
    api_prefix="/api/v1",
    debug=True,  # if set to False, authentication would be enabled
    storage_dir="resume_vault/",
    log_file="api_call_log.csv",
    # Models configuration
    transcriber_endpoint="http://13.233.246.91:8002/api/v1/transcribe",
    openai_key="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",
    # Service type
    service_type="async",
    # Endpoints configuration
    resume_parser_endpoint=True,
    front_end_point="http://127.0.0.1:8501",
    # API authentication configuration
    username="aiss@rbg.ai",
    password="demo@RBG2023",
    openssl_key="6f9c02d4e343479ca147ce7a8a15db6f3b47360f0e84f66404079f216815f193",
    openssl_algorithm="HS256",
    access_token_expire_minutes=30,
)
