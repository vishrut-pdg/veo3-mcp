import os
from mcp.server.fastmcp import FastMCP
from google import genai
from google.genai import types

PORT = int(os.environ.get("PORT", 8080))

mcp = FastMCP("Veo3-Vertex-MCP", host="0.0.0.0", port=PORT)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
OUTPUT_GCS_URI = os.environ.get("VIDEO_OUTPUT_GCS_URI")

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

VEO_MODEL = "veo-3.0-generate-001"


@mcp.tool()
def generate_video_text(
    prompt: str,
    sample_count: int = 1,
    resolution: str = "720p",
) -> str:
    """
    Generates an 8-second video from a text prompt using Google Veo 3.0 on Vertex AI.

    Args:
        prompt: The scene description.
        sample_count: Number of video samples to generate (1-4).
        resolution: Output resolution, e.g. "720p" or "1080p".
    """
    if not OUTPUT_GCS_URI:
        return "Error: VIDEO_OUTPUT_GCS_URI is not set on the server."

    try:
        operation = client.models.generate_videos(
            model=VEO_MODEL,
            prompt=prompt,
            config=types.GenerateVideosConfig(
                output_gcs_uri=OUTPUT_GCS_URI,
                number_of_videos=sample_count,
                resolution=resolution,
            ),
        )
        return (
            f"Video generation started. Operation name: {operation.name}. "
            f"Call fetch_video_result with this name to poll."
        )
    except Exception as e:
        return f"Error triggering video generation: {str(e)}"


@mcp.tool()
def fetch_video_result(operation_name: str) -> str:
    """
    Polls a Veo video generation operation. Returns a status message while
    in progress, or the GCS URIs of the generated videos when complete.

    Args:
        operation_name: The operation name returned from generate_video_text.
    """
    try:
        operation = types.GenerateVideosOperation(name=operation_name)
        operation = client.operations.get(operation)

        if not operation.done:
            return f"Operation {operation_name} is still in progress."
        if getattr(operation, "error", None):
            return f"Operation failed: {operation.error}"

        videos = getattr(operation.response, "generated_videos", None) or []
        uris = [v.video.uri for v in videos if v.video and v.video.uri]
        return f"Done. Generated {len(uris)} video(s): {uris}"
    except Exception as e:
        return f"Error fetching operation: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
