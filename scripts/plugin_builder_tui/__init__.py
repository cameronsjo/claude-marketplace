"""
Plugin Builder TUI - Modern terminal interface for Claude Code marketplace management.
"""

from .builder import (
    Asset,
    AssetType,
    Plugin,
    PluginBuilder,
    UsageInfo,
)

__all__ = [
    "PluginBuilder",
    "Asset",
    "AssetType",
    "Plugin",
    "UsageInfo",
]


def get_app():
    """Lazy import of PluginBuilderApp to avoid requiring textual for CLI."""
    from .app import PluginBuilderApp

    return PluginBuilderApp
