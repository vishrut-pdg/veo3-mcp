#!/usr/bin/env python3
"""
Build and publish script for mcp-veo3

This script builds the package and optionally publishes it to PyPI.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

def main():
    """Main build and publish workflow"""
    print("🚀 MCP Veo 3 Build and Publish Script")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"📁 Working directory: {project_root}")
    
    # Check if uv is available
    if not run_command(["uv", "--version"]):
        print("❌ uv is not installed. Please install uv first:")
        print("curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    print("✅ uv is available")
    
    # Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    dist_dir = project_root / "dist"
    if dist_dir.exists():
        import shutil
        shutil.rmtree(dist_dir)
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not run_command(["uv", "sync"]):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run tests
    print("\n🧪 Running tests...")
    if not run_command(["python", "examples/test_fastmcp_server.py"]):
        print("⚠️ Tests failed, but continuing with build...")
    
    # Build the package
    print("\n🔨 Building package...")
    if not run_command(["uv", "build"]):
        print("❌ Failed to build package")
        sys.exit(1)
    
    print("✅ Package built successfully!")
    
    # List built files
    if dist_dir.exists():
        print("\n📦 Built files:")
        for file in dist_dir.iterdir():
            print(f"  - {file.name}")
    
    # Ask about publishing
    publish = input("\n🚀 Publish to PyPI? (y/N): ").lower().strip()
    
    if publish == 'y':
        print("\n📤 Publishing to PyPI...")
        
        # Check if PYPI_API_TOKEN is set
        if not os.getenv("PYPI_API_TOKEN"):
            print("⚠️ PYPI_API_TOKEN environment variable not set")
            token = input("Enter your PyPI API token (or press Enter to skip): ").strip()
            if token:
                os.environ["PYPI_API_TOKEN"] = token
            else:
                print("❌ Cannot publish without API token")
                sys.exit(1)
        
        # Publish using uv
        if run_command(["uv", "publish", "--token", os.environ["PYPI_API_TOKEN"]]):
            print("✅ Successfully published to PyPI!")
            print("\n🎉 Package is now available:")
            print("   pip install mcp-veo3")
            print("   uvx mcp-veo3 --output-dir ~/Videos")
        else:
            print("❌ Failed to publish to PyPI")
            sys.exit(1)
    else:
        print("⏭️ Skipping PyPI publication")
        print("\nTo publish later, run:")
        print("  uv publish --token $PYPI_API_TOKEN")
    
    print("\n✅ Build process completed!")

if __name__ == "__main__":
    main()
