from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logger import logger  

# catches raised http exceptions 
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"Unhandled exception at {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "code": exc.status_code,
        },
    )

# validation errors
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error at {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": str(exc),
            "code": 422,
        },
    )

# unhandled exceptions 
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception at {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": f"Internal server error: {str(exc)}",
            "code": 500,
        },
    )
