"""Authentication and learning surface routers for DeepTutor."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from deeptutor.multi_user.learning_access import assert_learning_surface
from deeptutor.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# Learning surface defaults per preset
LEARNER_DEFAULT_SURFACES = ["chat", "reading"]


def _learning_surface_for_path(path: str) -> str:
    """Map API path to learning surface name.

    See deeptutor.api.routers.LEARNING_SURFACE_MAP for the mapping.
    """
    from deeptutor.api.routers import LEARNING_SURFACE_MAP
    return LEARNING_SURFACE_MAP.get(path, "")


@router.get("/surfaces", include_in_schema=False)
async def list_surfaces():
    """List available learning surfaces."""
    from deeptutor.api.routers import LEARNING_SURFACE_MAP
    return {"surfaces": list(LEARNING_SURFACE_MAP.keys())}


@router.get("/check-surface/{path:path}")
async def check_surface(path: str, db: Session = Depends(get_db)):
    """Check if the given path's learning surface is allowed for the user.

    This is used by the frontend to pre-validate that an endpoint will be
    accessible before making the request, avoiding the misleading empty state
    described in issue #1228.
    """
    surface = _learning_surface_for_path(path)
    if not surface:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No learning surface mapped for path: {path}",
        )
    return {"path": path, "surface": surface, "allowed": surface in LEARNER_DEFAULT_SURFACES}
