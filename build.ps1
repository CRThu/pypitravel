uv run nuitka src/pypitravel/cli.py `
    --onefile `
    --output-dir=build `
    --include-data-dir=src/pypitravel/static=static `
    --include-package=fastapi `
    --include-package=uvicorn `
    --include-package=httpx
