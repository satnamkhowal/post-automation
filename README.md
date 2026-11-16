# Brand Manager MCP

A narrow, safety-first MCP server for managing multiple Google Business Profile brands and locations.

## Scope (v0)

- Select an authorized brand and location.
- Read profile metadata.
- Draft a Google Business Profile update.
- Publish only after an explicit, per-publication confirmation token.
- Keep brand/account boundaries explicit so customer separation can be added later.

This first version does not connect to social networks, onboard customers, publish real posts, or require hosting.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
python -m brand_manager
```

The local server exposes an MCP endpoint at `http://localhost:8000/mcp` when run with the included entry point.

The default adapter is an in-memory demo adapter. It deliberately does not call Google or publish anything. Set `BRAND_MANAGER_ADAPTER=google` only after implementing and configuring the Google adapter.

## Required Google setup before live use

1. Create/select a Google Cloud project and request/obtain Business Profile API access.
2. Enable the required Business Profile APIs.
3. Configure the OAuth consent screen and a web OAuth client.
4. Use the `https://www.googleapis.com/auth/business.manage` scope.
5. Add the app redirect URI and store client credentials outside the repository.
6. Authorize the Google account(s) that own/manage the target profiles.
7. Test reads first; Google has no sandbox. Use `validateOnly` where supported for validation.

See `docs/setup.md` for the checklist and safety model.

## ChatGPT connection

This is an MCP server, which is the current plugin integration path. A hosted deployment must expose the `/mcp` endpoint over HTTPS. Do not connect a local or public server until its authentication, authorization, and write protections have been reviewed.

