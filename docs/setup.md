# Setup and safety checklist

## Architecture

The server separates:

- `Brand`: a logical customer/brand boundary.
- `Location`: one authorized Google Business Profile location.
- `ProfileProvider`: read/write adapter; the demo provider is safe and local.
- MCP tools: selection, reads, drafting, and confirmed publishing.

The provider interface is the seam for a real Google adapter. Future customer separation can map an authenticated tenant to a set of brands without changing the tool contract.

## Google prerequisites

Google's official Business Profile OAuth documentation says that requests require OAuth 2.0 and the `business.manage` scope. Google also requires Cloud project configuration, API enablement, OAuth credentials, and consent-screen setup. Business Profile APIs do not provide a sandbox; validate requests where `validateOnly` is supported.

Official references:

- https://developers.google.com/my-business/content/basic-setup
- https://developers.google.com/my-business/content/implement-oauth

## Write safety

`draft_update` returns a preview and a short-lived confirmation token. `publish_update` requires the exact token and an explicit `confirm=true`. The demo provider records the publication locally, but a future Google provider must pass the same guard before making a live API call.

Never put OAuth client secrets, access tokens, or refresh tokens in `.env`, source control, issue comments, or chat messages. Use a secret manager or local environment variables.

