


from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from ResumeParser.config import settings
from ResumeParser.services.parser_service import ResumeAsyncService
from ResumeParser.utils import retrieve_user_platform


resume_parser = ResumeAsyncService(
    debug_mode=settings.debug,
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Context manager to handle the startup and shutdown of the application."""
    if retrieve_user_platform() != "linux":
        logger.warning(
            "You are not running the application on Linux.\nThe application was tested"
            " on Ubuntu 22.04, so we cannot guarantee that it will work on other OS."
        )

    logger.info("Warmup initialization...")
    await resume_parser.inference_warmup()

    yield  # This is where the execution of the application starts

