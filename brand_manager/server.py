from mcp.server.fastmcp import FastMCP

from .core import DemoProvider, DraftStore

mcp = FastMCP("Brand Manager")
provider = DemoProvider()
drafts = DraftStore()


@mcp.tool()
def list_brands() -> list[dict]:
    """List brands authorized for the current account context."""
    return provider.list_brands()


@mcp.tool()
def list_locations(brand_id: str) -> list[dict]:
    """List locations for one selected brand."""
    return provider.list_locations(brand_id)


@mcp.tool()
def get_profile(location_id: str) -> dict:
    """Read profile metadata for a selected location."""
    return provider.get_profile(location_id)


@mcp.tool()
def draft_update(location_id: str, text: str, call_to_action: str | None = None) -> dict:
    """Create a preview; this does not publish anything."""
    if not text.strip():
        raise ValueError("Update text cannot be empty")
    return drafts.create(location_id, text.strip(), call_to_action)


@mcp.tool()
def publish_update(confirmation_token: str, confirm: bool = False) -> dict:
    """Publish one previously previewed update only with explicit confirmation."""
    preview = drafts.confirm(confirmation_token, confirm)
    return provider.publish(preview)

