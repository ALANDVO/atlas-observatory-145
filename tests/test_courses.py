"""Courses endpoint tests for DeepTutor API - issue #1228 fix.

Tests that learner accounts can access /api/courses without getting 403.
Previously, learner accounts with preset="learner" would get 403 on this
endpoint because /api/courses was not mapped to a learning surface.
"""

from fastapi.testclient import TestClient
from deeptutor.api.main import app


def test_courses_endpoint_returns_200():
    """GET /api/v1/courses returns 200 for all account types."""
    client = TestClient(app)
    resp = client.get("/api/v1/courses")
    assert resp.status_code == 200


def test_courses_endpoint_structure():
    """GET /api/v1/courses returns expected structure."""
    client = TestClient(app)
    resp = client.get("/api/v1/courses")
    assert resp.status_code == 200
    data = resp.json()
    assert "courses" in data
    assert "message" in data
    assert "No courses found" in data["message"]


def test_learning_surface_map_includes_courses():
    """Verify /api/courses is mapped to 'courses' surface."""
    from deeptutor.api.routers import LEARNING_SURFACE_MAP
    assert "/api/courses" in LEARNING_SURFACE_MAP
    assert LEARNING_SURFACE_MAP["/api/courses"] == "courses"


def test_assert_learning_surface_includes_courses_for_learners():
    """Verify assert_learning_surface defaults include 'courses' for learners."""
    from deeptutor.multi_user.learning_access import assert_learning_surface

    # This should not raise for learner default surfaces
    try:
        assert_learning_surface("courses")
    except Exception as e:
        assert False, f"assert_learning_surface('courses') raised: {e}"
