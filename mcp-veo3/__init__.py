"""
MCP Veo 3 Video Generation Server

A Model Context Protocol (MCP) server for generating videos using Google's Veo 3 API.
"""

__version__ = "1.0.0"
__author__ = "MCP Veo 3 Team"
__description__ = "MCP Server for Google Veo 3 Video Generation"

from .mcp_veo3 import Veo3Client, VideoGenerationConfig

__all__ = ["Veo3Client", "VideoGenerationConfig"]
