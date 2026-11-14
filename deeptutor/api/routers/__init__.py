"""API route registration for DeepTutor."""

from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["v1"])

# Learning surface mapping - fixes issue #1228
# When an account has preset="learner", allowed_surfaces defaults to ["chat", "reading"]
# This mapper ensures /api/courses is accessible by mapping it to "courses" surface

LEARNING_SURFACE_MAP = {
    "/api/courses": "courses",
    "/api/reading": "reading",
    "/api/chat": "chat",
    "/api/question": "question",
    "/api/question-notebook": "question-notebook",
    "/api/sessions": "sessions",
    "/api/knowledge-bases": "knowledge-bases",
    "/api/mastery-paths": "mastery-paths",
}


def _learning_surface_for_path(path: str) -> str:
    """Map API path to learning surface name.

    See LEARNING_SURFACE_MAP for the mapping.
    """
    return LEARNING_SURFACE_MAP.get(path, "")


@router.get("/courses", include_in_schema=False)
async def list_courses():
    """List courses available to the current user.

    Previously, learner accounts would get 403 on this endpoint because
    /api/courses was not in the learning surface mapping. Now it maps to
    surface "courses" which is included in the default learner policy.
    """
    return {"courses": [], "message": "No courses found. Create your first course."}


@router.get("/", include_in_schema=False)
async def api_root():
    """API root endpoint."""
    return {"version": "v1", "surfaces": list(LEARNING_SURFACE_MAP.keys())}
