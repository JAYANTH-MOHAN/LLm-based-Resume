

"""Routing the requested endpoints to the API."""

from fastapi import APIRouter

from ResumeParser.config import settings
from ResumeParser.router.authentication import router as auth_router
from ResumeParser.router.v1.resume_parser_endpoint import router as resume_parser_router

api_router = APIRouter()

async_routers = (
    ("resume_parser_endpoint", resume_parser_router, "/parse", "async"),
)


if settings.service_type == "async":
    routers = async_routers
else:
    raise ValueError(f"Invalid service type: {settings.service_type}")

for router_items in routers:
    endpoint, router, prefix, tags = router_items

    # If the endpoint is enabled, include it in the API.
    if getattr(settings, endpoint) is True:
        api_router.include_router(router, prefix=prefix, tags=[tags])
