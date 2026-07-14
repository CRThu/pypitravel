uv sync --extra gui --group dev
uv run nuitka src/pypitravel/ `
    --onefile `
    --output-dir=build `
    --python-flag=-m `
    --no-deployment-flag=excluded-module-usage `
    --experimental=force-dependencies-pefile `
    --include-data-dir=src/pypitravel/static=pypitravel/static `
    --include-package=fastapi `
    --include-package=uvicorn `
    --include-package=httpx `
    --include-package=webview `
    --disable-plugins=pywebview `
    --nofollow-import-to=webview.platforms.android `
    --nofollow-import-to=webview.platforms.cocoa `
    --nofollow-import-to=webview.platforms.gtk `
    --nofollow-import-to=webview.platforms.qt `
    --nofollow-import-to=webview.platforms.cef