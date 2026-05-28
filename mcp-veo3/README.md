# MCP Veo 3 Video Generation Server

A Model Context Protocol (MCP) server that provides video generation capabilities using Google's Veo 3 API through the Gemini API. Generate high-quality videos from text prompts or images with realistic motion and audio.

## Features

- 🎬 **Text-to-Video**: Generate videos from descriptive text prompts
- 🖼️ **Image-to-Video**: Animate static images with motion prompts
- 🎵 **Audio Generation**: Native audio generation with Veo 3 models
- 🎨 **Multiple Models**: Support for Veo 3, Veo 3 Fast, and Veo 2
- 📐 **Aspect Ratios**: Widescreen (16:9) and portrait (9:16) support
- ❌ **Negative Prompts**: Specify what to avoid in generated videos
- 📁 **File Management**: List and manage generated videos
- ⚡ **Async Processing**: Non-blocking video generation with progress tracking

## Supported Models

| Model | Description | Speed | Quality | Audio |
|-------|-------------|-------|---------|-------|
| `veo-3.0-generate-preview` | Latest Veo 3 with highest quality | Slower | Highest | ✅ |
| `veo-3.0-fast-generate-preview` | Optimized for speed and business use | Faster | High | ✅ |
| `veo-2.0-generate-001` | Previous generation model | Medium | Good | ❌ |

## 📦 Installation Options

```bash
# Run without installing (recommended)
uvx mcp-veo3 --output-dir ~/Videos/Generated

# Install globally
pip install mcp-veo3

# Development install
git clone && cd mcp-veo3 && uv sync
```

## Installation

### Option 1: Direct Usage (Recommended)
```bash
# No installation needed - run directly with uvx
uvx mcp-veo3 --output-dir ~/Videos/Generated
```

### Option 2: Development Setup
1. **Clone this directory**:
   ```bash
   git clone https://github.com/dayongd1/mcp-veo3
   cd mcp-veo3
   ```

2. **Install with uv**:
   ```bash
   uv sync
   ```
   
   Or use the automated setup:
   ```bash
   python setup.py
   ```

3. **Set up API key**:
   - Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create `.env` file: `cp env_example.txt .env`
   - Edit `.env` and add your `GEMINI_API_KEY`
   - Or set environment variable: `export GEMINI_API_KEY='your_key'`

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
DEFAULT_OUTPUT_DIR=generated_videos
DEFAULT_MODEL=veo-3.0-generate-preview
DEFAULT_ASPECT_RATIO=16:9
PERSON_GENERATION=dont_allow
POLL_INTERVAL=10
MAX_POLL_TIME=600
```

### MCP Client Configuration

#### Option 1: Using uvx (Recommended - after PyPI publication)
```json
{
  "mcpServers": {
    "veo3": {
      "command": "uvx",
      "args": ["mcp-veo3", "--output-dir", "~/Videos/Generated"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### Option 2: Using uv run (Development)
```json
{
  "mcpServers": {
    "veo3": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-veo3", "mcp-veo3", "--output-dir", "~/Videos/Generated"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### Option 3: Direct Python
```json
{
  "mcpServers": {
    "veo3": {
      "command": "python",
      "args": ["/path/to/mcp-veo3/mcp_veo3.py", "--output-dir", "~/Videos/Generated"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**CLI Arguments:**
- `--output-dir` (required): Directory to save generated videos
- `--api-key` (optional): Gemini API key (overrides environment variable)

## Available Tools

### 1. generate_video

Generate a video from a text prompt.

**Parameters:**
- `prompt` (required): Text description of the video
- `model` (optional): Model to use (default: veo-3.0-generate-preview)
- `negative_prompt` (optional): What to avoid in the video
- `aspect_ratio` (optional): 16:9 or 9:16 (default: 16:9)
- `output_dir` (optional): Directory to save videos (default: generated_videos)

**Example:**
```json
{
  "prompt": "A close up of two people staring at a cryptic drawing on a wall, torchlight flickering. A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'",
  "model": "veo-3.0-generate-preview",
  "aspect_ratio": "16:9"
}
```

### 2. generate_video_from_image

Generate a video from a starting image and motion prompt.

**Parameters:**
- `prompt` (required): Text description of the desired motion/action
- `image_path` (required): Path to the starting image file
- `model` (optional): Model to use (default: veo-3.0-generate-preview)
- `negative_prompt` (optional): What to avoid in the video
- `aspect_ratio` (optional): 16:9 or 9:16 (default: 16:9)
- `output_dir` (optional): Directory to save videos (default: generated_videos)

**Example:**
```json
{
  "prompt": "The person in the image starts walking forward with a confident stride",
  "image_path": "./images/person_standing.jpg",
  "model": "veo-3.0-generate-preview"
}
```

### 3. list_generated_videos

List all generated videos in the output directory.

**Parameters:**
- `output_dir` (optional): Directory to list videos from (default: generated_videos)

### 4. get_video_info

Get detailed information about a video file.

**Parameters:**
- `video_path` (required): Path to the video file

## Usage Examples

### Basic Text-to-Video Generation

```python
# Through MCP client
result = await mcp_client.call_tool("generate_video", {
    "prompt": "A majestic waterfall in a lush forest with sunlight filtering through the trees",
    "model": "veo-3.0-generate-preview"
})
```

### Image-to-Video with Negative Prompt

```python
result = await mcp_client.call_tool("generate_video_from_image", {
    "prompt": "The ocean waves gently crash against the shore",
    "image_path": "./beach_scene.jpg",
    "negative_prompt": "people, buildings, artificial structures",
    "aspect_ratio": "16:9"
})
```

### Creative Animation

```python
result = await mcp_client.call_tool("generate_video", {
    "prompt": "A stylized animation of a paper airplane flying through a colorful abstract landscape",
    "model": "veo-3.0-fast-generate-preview",
    "aspect_ratio": "16:9"
})
```

## Prompt Writing Tips

### Effective Prompts
- **Be specific**: Include details about lighting, mood, camera angles
- **Describe motion**: Specify the type of movement you want
- **Set the scene**: Include environment and atmospheric details
- **Mention style**: Cinematic, realistic, animated, etc.

### Example Prompts

**Cinematic Realism:**
```
A tracking drone view of a red convertible driving through Palm Springs in the 1970s, warm golden hour sunlight, long shadows, cinematic camera movement
```

**Creative Animation:**
```
A stylized animation of a large oak tree with leaves blowing vigorously in strong wind, peaceful countryside setting, warm lighting
```

**Dialogue Scene:**
```
Close-up of two people having an intense conversation in a dimly lit room, dramatic lighting, one person gesturing emphatically while speaking
```

### Negative Prompts
Describe what you **don't** want to see:
- ❌ Don't use "no" or "don't": `"no cars"` 
- ✅ Do describe unwanted elements: `"cars, vehicles, traffic"`

## Limitations

- **Generation Time**: 11 seconds to 6 minutes depending on complexity
- **Video Length**: 8 seconds maximum
- **Resolution**: 720p output
- **Storage**: Videos are stored on Google's servers for 2 days only
- **Regional Restrictions**: Person generation defaults to "dont_allow" in EU/UK/CH/MENA
- **Watermarking**: All videos include SynthID watermarks

## 🚨 Troubleshooting

**"API key not found"**
```bash
# Set your Gemini API key
export GEMINI_API_KEY='your_api_key_here'
# Or add to .env file
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

**"Output directory not accessible"**
```bash
# Ensure the output directory exists and is writable
mkdir -p ~/Videos/Generated
chmod 755 ~/Videos/Generated
```

**"Video generation timeout"**
```bash
# Try using the fast model for testing
uvx mcp-veo3 --output-dir ~/Videos
# Then use: model="veo-3.0-fast-generate-preview"
```

**"Import errors"**
```bash
# Install/update dependencies
uv sync
# Or with pip
pip install -r requirements.txt
```

## Error Handling

The server handles common errors gracefully:

- **Invalid API Key**: Clear error message with setup instructions
- **File Not Found**: Validation for image paths in image-to-video
- **Generation Timeout**: Configurable timeout with progress updates
- **Model Errors**: Fallback error handling with detailed messages

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Code Formatting

```bash
# Format code
black mcp_veo3.py

# Check linting
flake8 mcp_veo3.py

# Type checking
mypy mcp_veo3.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📚 Links

- **PyPI**: https://pypi.org/project/mcp-veo3/
- **GitHub**: https://github.com/dayongd1/mcp-veo3
- **MCP Docs**: https://modelcontextprotocol.io/
- **Veo 3 API**: https://ai.google.dev/gemini-api/docs/video

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Documentation**: [Google Veo 3 API Docs](https://ai.google.dev/gemini-api/docs/video)
- **API Key**: [Get your Gemini API key](https://makersuite.google.com/app/apikey)
- **Issues**: Report bugs and feature requests in the GitHub issues

## Changelog

### v1.0.1
- **🔧 API Fix**: Updated to match official Veo 3 API specification
- **Removed unsupported parameters**: aspect_ratio, negative_prompt, person_generation
- **Simplified API calls**: Now using only model and prompt parameters as per official docs
- **Fixed video generation errors**: Resolved "unexpected keyword argument" issues
- **Updated documentation**: Added notes about current API limitations

### v1.0.0
- Initial release
- Support for Veo 3, Veo 3 Fast, and Veo 2 models
- Text-to-video and image-to-video generation
- FastMCP framework with progress tracking
- Comprehensive error handling and logging
- File management utilities
- uv/uvx support for easy installation

---

**Built with FastMCP** | **Python 3.10+** | **MIT License**
