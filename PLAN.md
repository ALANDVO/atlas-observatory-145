# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

foundation-skeleton

## Roadmap

### foundation-skeleton — FastAPI/React skeleton with core workflow

Status: done

Acceptance:
- FastAPI app starts and responds at /health
- GET / returns API root information
- GET /api/v1/courses returns 200 for learner accounts
- Learning surface mapping: /api/courses -> courses surface
- assert_learning_surface includes courses in learner defaults

Implementation: `deeptutor/api/main.py - FastAPI application entry point`, `deeptutor/api/routers/__init__.py - API route registration with LEARNING_SURFACE_MAP`, `deeptutor/multi_user/learning_access.py - assert_learning_surface with courses in learner defaults`, `deeptutor/api/routers/auth.py - surface checking endpoint`

Tests: `tests/test_health.py - health endpoint test`, `tests/test_courses.py - courses endpoint test with learner preset`

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
