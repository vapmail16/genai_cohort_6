# SaaS project scaffold

Empty layout for a backend and frontend SaaS application. Only folders and placeholders are present; add languages, frameworks, and tooling when you initialize each part.

## Layout

| Path | Intent |
|------|--------|
| `backend/src` | API, domain, and application layers |
| `backend/tests` | Backend tests (`unit`, `integration`, `e2e`) |
| `backend/config` | Environment and service configuration samples |
| `backend/scripts` | Operational scripts (migrations, seeds, jobs) |
| `frontend/src` | Web UI source |
| `frontend/tests` | Frontend tests (`unit`, `e2e`) |
| `frontend/public` | Static assets served as-is |
| `frontend/config` | Build and environment configuration |
| `packages/shared-contracts` | Optional shared API/types between backend and frontend |
| `infra/terraform` | Infrastructure-as-code entry point |
| `infra/containers` | Container definitions and compose files |
| `docs` | Product and engineering documentation |
| `.github/workflows` | CI/CD workflow definitions |

Empty directories are tracked with `.gitkeep` files.
