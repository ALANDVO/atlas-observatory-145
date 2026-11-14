"""Learning access control for multi-user DeepTutor."""

from fastapi import HTTPException, status

# Import the surface mapper from auth routers
# This mirrors the _learning_surface_for_path from deeptutor.api.routers.auth
try:
    from deeptutor.api.routers import _learning_surface_for_path
except ImportError:
    # Fallback inline implementation for standalone use
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
        return LEARNING_SURFACE_MAP.get(path, "")


def assert_learning_surface(required_surface: str, user_surfaces: list[str] | None = None):
    """Assert that the user has the required learning surface.

    Raises 403 if the user does not have the required surface.

    Args:
        required_surface: The surface needed to access the endpoint.
        user_surfaces: List of surfaces the user is allowed. Defaults to
                       ["chat", "reading", "courses"] for learner accounts
                       (includes courses to fix issue #1228).

    Raises:
        HTTPException: 403 if user does not have the required surface.
    """
    if user_surfaces is None:
        # Default learner preset surfaces - includes "courses" to fix issue #1228
        # See: https://github.com/HKUDS/DeepTutor/issues/1228
        user_surfaces = ["chat", "reading", "courses"]

    if required_surface not in user_surfaces:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Learning surface '{required_surface}' not allowed for this account. "
                   f"Allowed surfaces: {user_surfaces}",
        )
