


"""Logging module to add a logging middleware to the ResumeParser."""

import sys
import time
import uuid
from typing import Any, Awaitable, Callable, Tuple

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log requests, responses, errors and execution time."""

    def __init__(self, app: ASGIApp, debug_mode: bool) -> None:
        """Initialize the middleware."""
        super().__init__(app)
        logger.remove()
        logger.add(
            sys.stdout,
            level=(
                "DEBUG" if debug_mode else "INFO"
            ),  # Avoid logging debug messages in prod
        )

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Dispatch a request and log it, along with the response and any errors.

        Args:
            request: The request to dispatch.
            call_next: The next middleware to call.

        Returns:
            The response from the next middleware.
        """
        start_time = time.time()
        tracing_id = uuid.uuid4()

        if request.method == "POST":
            logger.info(f"Task [{tracing_id}] | {request.method} {request.url}")
        else:
            logger.info(f"{request.method} {request.url}")

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(
            f"Task [{tracing_id}] | Status: {response.status_code}, Time:"
            f" {process_time:.4f} secs"
        )

        return response


def time_and_tell(
    func: Callable, func_name: str, debug_mode: bool
) -> Tuple[Any, float]:
    """
    This decorator logs the execution time of a function only if the debug setting is True.

    Args:
        func: The function to call in the wrapper.
        func_name: The name of the function for logging purposes.
        debug_mode: The debug setting for logging purposes.

    Returns:
        The appropriate wrapper for the function.
    """
    start_time = time.time()
    result = func()
    process_time = time.time() - start_time

    if debug_mode:
        logger.debug(f"{func_name} executed in {process_time:.4f} secs")

    return result, process_time
