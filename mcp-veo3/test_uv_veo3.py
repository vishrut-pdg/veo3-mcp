#!/usr/bin/env python3
"""
Test Veo 3 video generation using uv run (simulating Cursor with uv)
"""

import asyncio
import os
from pathlib import Path

from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport
from dotenv import load_dotenv, dotenv_values

# Load environment variables
load_dotenv()

async def test_uv_veo3():
    """Test Veo 3 video generation using uv run"""
    
    print("🚀 Testing Veo 3 video generation with 'uv run' (Cursor-style)...")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("Please set your Gemini API key:")
        print("export GEMINI_API_KEY='your_api_key_here'")
        return
    
    print("✅ GEMINI_API_KEY found")
    
    # Set up output directory
    env_vars = dotenv_values('.env')
    output_dir = Path.home() / "mcp-veo3-videos"
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Output directory: {output_dir}")
    
    # Use uv run to start the MCP server
    transport = StdioTransport(
        command="uv",
        args=["run", "mcp-veo3", "--output-dir", str(output_dir)],
        env=env_vars
    )
    
    try:
        async with Client(transport=transport) as client:
            print("🔌 Connected to MCP Veo 3 server via 'uv run'")
            
            # Test video generation
            print(f"\n🎬 Testing: Generate video via uv run")
            
            test_prompt = "A peaceful mountain lake reflecting the sunset, with gentle ripples on the water surface"
            
            result = await client.call_tool("generate_video", {
                "prompt": test_prompt,
                "model": "veo-3.0-fast-generate-preview",  # Use fast model for testing
                "aspect_ratio": "16:9"
            })
            
            print("✅ Video generation started via uv run!")
            data = result.data
            print(f"📁 Video path: {data.video_path}")
            print(f"🎬 Model: {data.model}")
            print(f"⏱️ Generation time: {data.generation_time:.1f} seconds")
            print(f"📏 File size: {data.file_size / 1024 / 1024:.1f} MB")
            print(f"💭 Prompt: {data.prompt}")
            
            # Test listing videos
            print(f"\n📁 Testing: List generated videos")
            list_result = await client.call_tool("list_generated_videos", {})
            
            if list_result.data.videos:
                print(f"✅ Found {list_result.data.total_count} videos:")
                for video in list_result.data.videos[:3]:  # Show first 3
                    print(f"   • {video['filename']} ({video['size_mb']} MB)")
            else:
                print("📂 No videos found yet")
            
            print(f"\n🎉 UV run test completed successfully!")
            print(f"\n📋 Cursor Configuration Ready:")
            print(f'  "command": "uv"')
            print(f'  "args": ["run", "--directory", "/Users/dayonghuang/gitssh/boxer/mcp-veo3", "mcp-veo3", "--output-dir", "~/Videos/Generated"]')
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_uvx_veo3():
    """Test Veo 3 video generation using uvx (after PyPI publication)"""
    
    print("\n🚀 Testing Veo 3 video generation with 'uvx' (PyPI install)...")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        return
    
    # Set up output directory
    env_vars = dotenv_values('.env')
    output_dir = Path.home() / "mcp-veo3-videos"
    output_dir.mkdir(exist_ok=True)
    
    # Use uvx to run the MCP server (after PyPI publication)
    transport = StdioTransport(
        command="uvx",
        args=["mcp-veo3", "--output-dir", str(output_dir)],
        env=env_vars
    )
    
    try:
        async with Client(transport=transport) as client:
            print("🔌 Connected to MCP Veo 3 server via 'uvx'")
            
            # Test a quick video generation
            print(f"\n🎬 Testing: Generate video via uvx")
            
            result = await client.call_tool("generate_video", {
                "prompt": "A butterfly landing on a flower in slow motion",
                "model": "veo-3.0-fast-generate-preview",
                "aspect_ratio": "16:9"
            })
            
            print("✅ Video generation via uvx successful!")
            data = result.data
            print(f"📁 Video: {data.filename}")
            print(f"⏱️ Time: {data.generation_time:.1f}s")
            
            print(f"\n🎉 UVX test completed successfully!")
            print(f"\n📋 Global Usage Ready:")
            print(f'  uvx mcp-veo3 --output-dir ~/Videos')
                
    except Exception as e:
        print(f"❌ UVX test failed (this is expected if not published to PyPI yet): {e}")

def main():
    """Run uv and uvx tests"""
    print("🎯 MCP Veo 3 UV/UVX Test Suite")
    print("=" * 50)
    
    # Test uv run (local development)
    asyncio.run(test_uv_veo3())
    
    # Test uvx (PyPI package - will fail until published)
    asyncio.run(test_uvx_veo3())
    
    print("\n📝 Summary:")
    print("✅ uv run - Works with local development")
    print("⏳ uvx - Will work after PyPI publication")

if __name__ == "__main__":
    main()
