#!/usr/bin/env python3
"""
Image-to-video test script for Veo 3

This script demonstrates image-to-video generation using the MCP Veo 3 server.
It creates a sample image first, then generates a video from it.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path to import the MCP server
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_veo3 import Veo3Client, VideoGenerationConfig

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = ImageDraw = ImageFont = None

def create_sample_image():
    """Create a sample image for testing image-to-video"""
    if not Image:
        print("❌ PIL (Pillow) not installed. Install with: pip install Pillow")
        return None
    
    # Create a simple landscape image
    width, height = 1280, 720  # 16:9 aspect ratio
    image = Image.new('RGB', (width, height), color='skyblue')
    draw = ImageDraw.Draw(image)
    
    # Draw a simple landscape
    # Ground
    draw.rectangle([0, height//2, width, height], fill='green')
    
    # Mountains
    mountain_points = [
        (0, height//2),
        (width//4, height//4),
        (width//2, height//3),
        (3*width//4, height//5),
        (width, height//2)
    ]
    draw.polygon(mountain_points, fill='gray')
    
    # Sun
    sun_center = (width - 100, 100)
    sun_radius = 50
    draw.ellipse([
        sun_center[0] - sun_radius,
        sun_center[1] - sun_radius,
        sun_center[0] + sun_radius,
        sun_center[1] + sun_radius
    ], fill='yellow')
    
    # Save the image
    image_path = Path(__file__).parent / "sample_landscape.jpg"
    image.save(image_path, "JPEG", quality=95)
    print(f"📸 Created sample image: {image_path}")
    
    return str(image_path)

async def test_image_to_video():
    """Test image-to-video generation"""
    print("🖼️ Testing Image-to-Video Generation")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("Please set your Gemini API key:")
        print("export GEMINI_API_KEY='your_api_key_here'")
        return
    
    # Create sample image
    image_path = create_sample_image()
    if not image_path:
        return
    
    try:
        # Initialize client
        print("🔧 Initializing Veo 3 client...")
        client = Veo3Client(api_key)
        
        # Configure generation
        config = VideoGenerationConfig(
            model="veo-3.0-fast-generate-preview",
            aspect_ratio="16:9",
            output_dir="test_videos"
        )
        
        # Motion prompt for the landscape
        prompt = "The sun slowly moves across the sky while clouds drift peacefully overhead, creating moving shadows on the mountains"
        
        print(f"🖼️ Source image: {image_path}")
        print(f"📝 Motion prompt: {prompt}")
        print(f"🎬 Model: {config.model}")
        print("\n🚀 Starting image-to-video generation...")
        print("⏱️  This may take 1-6 minutes...")
        
        # Generate video from image
        result = await client.generate_video(prompt, config, image_path=image_path)
        
        # Display results
        if result["success"]:
            print("\n✅ Image-to-video generation completed!")
            print(f"📁 Video file: {result['video_path']}")
            print(f"🖼️ Source image: {image_path}")
            print(f"⏱️ Generation time: {result['generation_time']:.1f} seconds")
            print(f"📏 File size: {result['file_size'] / 1024 / 1024:.1f} MB")
        else:
            print(f"\n❌ Image-to-video generation failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

async def test_with_existing_image():
    """Test with an existing image file"""
    print("\n📁 Testing with User-Provided Image")
    print("=" * 50)
    
    # Look for common image files in the current directory
    current_dir = Path(__file__).parent
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp']
    
    existing_images = []
    for ext in image_extensions:
        existing_images.extend(current_dir.glob(f"*{ext}"))
        existing_images.extend(current_dir.glob(f"*{ext.upper()}"))
    
    if not existing_images:
        print("📂 No existing image files found in examples directory")
        print("💡 To test with your own image:")
        print("   1. Copy an image file to the examples directory")
        print("   2. Run this script again")
        return
    
    # Use the first found image
    image_path = str(existing_images[0])
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        return
    
    try:
        client = Veo3Client(api_key)
        
        config = VideoGenerationConfig(
            model="veo-3.0-fast-generate-preview",
            aspect_ratio="16:9",
            output_dir="test_videos"
        )
        
        # Generic motion prompt
        prompt = "Gentle camera movement revealing more of the scene, with natural lighting changes and subtle motion"
        
        print(f"🖼️ Using existing image: {image_path}")
        print(f"📝 Motion prompt: {prompt}")
        print("\n🚀 Starting generation...")
        
        result = await client.generate_video(prompt, config, image_path=image_path)
        
        if result["success"]:
            print("\n✅ Generation with existing image completed!")
            print(f"📁 Video file: {result['video_path']}")
        else:
            print(f"\n❌ Generation failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

async def main():
    """Run all image-to-video tests"""
    print("🎯 Image-to-Video Test Suite")
    print("=" * 50)
    
    await test_image_to_video()
    await test_with_existing_image()
    
    print("\n🎉 Image-to-video test suite completed!")
    print("\n💡 Tips:")
    print("- Image-to-video works best with clear, well-lit images")
    print("- Describe the motion you want to see in your prompt")
    print("- Higher resolution source images generally produce better results")

if __name__ == "__main__":
    asyncio.run(main())
