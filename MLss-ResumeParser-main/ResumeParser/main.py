

"""Main API module of the ResumeParser."""

from fastapi import Depends, FastAPI
from fastapi import status as http_status
from fastapi.responses import HTMLResponse

from ResumeParser.config import settings
from ResumeParser.dependencies import lifespan
from ResumeParser.logging import LoggingMiddleware
from ResumeParser.router.authentication import get_current_user
from ResumeParser.router.v1.endpoints import api_router, auth_router

# Main application instance creation
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_prefix}/openapi.json",
    debug=settings.debug,
    lifespan=lifespan,
)

# Add logging middleware
app.add_middleware(LoggingMiddleware, debug_mode=settings.debug)

# Include the appropriate routers based on the settings
if settings.debug is False:
    app.include_router(auth_router, tags=["authentication"])
    app.include_router(
        api_router, prefix=settings.api_prefix, dependencies=[Depends(get_current_user)]
    )
else:
    app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/", tags=["status"])
async def home() -> HTMLResponse:
    """Root endpoint returning a simple HTML page with the project info."""
    content = f"""
    <!DOCTYPE html>
<html>
<head>
    <title>{settings.project_name}</title>
    <link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">
</head>

<body class=" text-center flex flex-col h-[100%] bg-gray-100 text-gray-700">
    <div class="p-4">
        <h1 class="text-4xl items-start font-medium">{settings.project_name}</h1>
         <p class="text-gray-600">Version: {settings.version}</p>
        <a href="/docs">
            <button class="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Docs</button>
        </a>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=content, media_type="text/html")


@app.get("/healthz", status_code=http_status.HTTP_200_OK, tags=["status"])
async def health() -> dict:
    """Health check endpoint. Important for Kubernetes liveness probe."""
    return {"status": "ok"}
