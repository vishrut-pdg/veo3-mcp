# Veo 3 MCP Server Examples

This directory contains example scripts demonstrating how to use the Veo 3 MCP server.

## Prerequisites

1. **Set up your API key**:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

2. **Install dependencies**:
   ```bash
   cd ..
   pip install -r requirements.txt
   ```

## Example Scripts

### 1. `test_basic_generation.py`
Tests basic text-to-video generation capabilities.

**Features tested:**
- Simple text-to-video generation
- Video generation with negative prompts
- Different model options

**Run:**
```bash
python test_basic_generation.py
```

### 2. `test_image_to_video.py`
Tests image-to-video generation capabilities.

**Features tested:**
- Creating sample images for testing
- Image-to-video generation
- Working with existing image files

**Run:**
```bash
python test_image_to_video.py
```

### 3. `test_mcp_client.py`
Tests the MCP server through proper MCP protocol communication.

**Features tested:**
- MCP server initialization
- Tool listing
- Video generation through MCP calls
- Video file management

**Run:**
```bash
python test_mcp_client.py
```

### 4. `test_fastmcp_server.py`
Tests the updated FastMCP-based server functionality.

**Features tested:**
- Server startup and dependency checks
- Configuration validation
- FastMCP framework compatibility

**Run:**
```bash
python test_fastmcp_server.py
```

### 5. `test_uv_veo3.py` (New)
Tests uv and uvx integration for the Veo 3 server.

**Features tested:**
- uv run integration (development)
- uvx integration (after PyPI publication)
- Cursor-style MCP client usage

**Run:**
```bash
python test_uv_veo3.py
```

## Expected Output

### Successful Generation
```
✅ Video generated successfully!
📁 File: test_videos/veo3_video_20240115_143022.mp4
🎬 Model: veo-3.0-fast-generate-preview
⏱️ Generation time: 45.3 seconds
📏 File size: 12.4 MB
```

### Common Issues

1. **API Key Missing**:
   ```
   ❌ Error: GEMINI_API_KEY environment variable not set
   ```
   **Solution**: Set your Gemini API key as shown above.

2. **Generation Timeout**:
   ```
   ❌ Video generation timed out after 600 seconds
   ```
   **Solution**: Try again during off-peak hours or use a simpler prompt.

3. **Invalid Image Path**:
   ```
   ❌ Error: Image file not found: /path/to/image.jpg
   ```
   **Solution**: Check that the image file exists and the path is correct.

## Tips for Testing

### Effective Test Prompts

**Short and Simple** (faster generation):
- "A gentle ocean wave on a beach"
- "Clouds moving across a blue sky"
- "A flower swaying in the breeze"

**Detailed Cinematic** (higher quality):
- "A tracking shot of a red car driving through a desert landscape at golden hour"
- "Close-up of raindrops falling on a window with soft lighting"

### Model Selection for Testing

- **veo-3.0-fast-generate-preview**: Use for quick testing (faster)
- **veo-3.0-generate-preview**: Use for final/production videos (higher quality)
- **veo-2.0-generate-001**: Use for comparison or when audio isn't needed

### Monitoring Generation

The scripts provide progress updates:
- Initial request confirmation
- Polling status every 10 seconds
- Final results with timing and file info

## Troubleshooting

### Server Won't Start
```bash
# Check if all dependencies are installed
pip list | grep -E "(mcp|google-genai)"

# Try running the server directly
python ../mcp_veo3.py
```

### Generation Takes Too Long
- Try simpler prompts
- Use `veo-3.0-fast-generate-preview` model
- Test during off-peak hours
- Check your internet connection

### File Permissions
```bash
# Ensure the examples directory is writable
chmod +w .
mkdir -p test_videos
```

## Output Files

Generated videos are saved in:
- `test_videos/` - For basic generation tests
- `mcp_test_videos/` - For MCP client tests

Files are named with timestamps: `veo3_video_YYYYMMDD_HHMMSS.mp4`

## Next Steps

After running these examples successfully:

1. **Integrate with your MCP client** using the configuration in the main README
2. **Experiment with different prompts** to understand Veo 3's capabilities
3. **Try image-to-video** with your own images
4. **Explore different models** for various use cases
