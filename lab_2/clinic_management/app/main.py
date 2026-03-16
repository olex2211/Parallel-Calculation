from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.router import router
from app.core.config import settings
from app.core.exceptions import (
    BusinessRuleException,
    ConflictException,
    EntityNotFoundException,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Medical Clinic Management System — Lab Work #2",
    version="1.0.0",
)


# Exception handlers
@app.exception_handler(EntityNotFoundException)
async def entity_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "NOT_FOUND", "message": str(exc)},
    )


@app.exception_handler(BusinessRuleException)
async def business_rule_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "BUSINESS_RULE_VIOLATION", "message": str(exc)},
    )


@app.exception_handler(ConflictException)
async def conflict_handler(request, exc):
    return JSONResponse(
        status_code=409,
        content={"error": "CONFLICT", "message": str(exc)},
    )


# Routers
app.include_router(router)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}


#NOTE visits, payments not 404 but 200