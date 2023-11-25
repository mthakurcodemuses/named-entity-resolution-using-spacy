from fastapi import APIRouter, status

admin_router = APIRouter()
@admin_router.get("/health-check", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}
