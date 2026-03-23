# Changelog

All notable changes to NetSec-Container will be documented in this file.

## [Unreleased] - 2026-03-23

### Fixed
- All ruff lint errors across `src/` and `tests/` (30 issues, all auto-fixed):
  - Removed 29 unused imports (`asyncio`, `subprocess`, `re`, `typing.*`,
    `fastapi.File`, `fastapi.UploadFile`, `fastapi.HTTPException`,
    `fastapi.staticfiles.StaticFiles`, `fastapi.responses.FileResponse`,
    `fastapi.responses.JSONResponse`, `pathlib.Path`, `tempfile`,
    `ContainerScanner`)
  - Stripped extraneous `f` prefix from one f-string without placeholders
