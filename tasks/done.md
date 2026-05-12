# Done

## Repository Foundation

- Created `AGENTS.md` global operating contract.
- Created persistent specs in `specs/`.
- Created OpenCode configuration with planner, implementer, reviewer, and debugger agents.
- Created reusable skills and prompts.
- Created task memory files.
- Created validation and Ralph loop scripts.
- Validated with `bash scripts/validate.sh`.
- Published initial `main` branch.

## Web App Shell

- Added FastAPI/Pydantic backend shell.
- Added `/api/health` endpoint.
- Added mocked `/api/triage` endpoint returning schema-valid structured output.
- Added Vite/React/TypeScript frontend shell.
- Added structured result rendering, loading state, error state, and safety notice.
- Extended validation to cover frontend and backend tooling.
- Opened PR: https://github.com/djairofilho/sus-gemma4/pull/2
