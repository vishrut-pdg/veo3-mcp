import os
from datetime import timedelta
from mcp.server.fastmcp import FastMCP
from google import genai
from google.genai import types
from google.cloud import storage

PORT = int(os.environ.get("PORT", 8080))

mcp = FastMCP("Veo3-Vertex-MCP", host="0.0.0.0", port=PORT)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
OUTPUT_GCS_URI = os.environ.get("VIDEO_OUTPUT_GCS_URI")

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

VEO_MODEL = "veo-3.0-generate-001"

_storage_client = storage.Client(project=PROJECT_ID) if PROJECT_ID else None


def _parse_gcs_uri(uri: str) -> tuple[str, str]:
    path = uri.removeprefix("gs://")
    bucket, _, prefix = path.partition("/")
    return bucket, prefix


def _infer_image_mime_type(uri: str) -> str:
    lower = uri.lower()
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".webp"):
        return "image/webp"
    return "image/jpeg"


def _signed_url(gcs_uri: str, hours: int = 24) -> str:
    bucket_name, blob_name = _parse_gcs_uri(gcs_uri)
    blob = _storage_client.bucket(bucket_name).blob(blob_name)
    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(hours=hours),
        method="GET",
    )


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
        lines = []
        for v in videos:
            if not (v.video and v.video.uri):
                continue
            gcs_uri = v.video.uri
            name = gcs_uri.rsplit("/", 1)[-1]
            try:
                url = _signed_url(gcs_uri)
                lines.append(f"- [{name}]({url}) — playable for 24h. Source: `{gcs_uri}`")
            except Exception as sig_err:
                lines.append(f"- {gcs_uri} (signed URL failed: {sig_err})")
        if not lines:
            return "Done, but no video URIs found in the response."
        return f"Done. Generated {len(lines)} video(s):\n" + "\n".join(lines)
    except Exception as e:
        return f"Error fetching operation: {str(e)}"


@mcp.tool()
def generate_video_from_image(
    prompt: str,
    image_gcs_uri: str,
    sample_count: int = 1,
    resolution: str = "720p",
) -> str:
    """
    Generates a video animated from a starting image using Google Veo 3.0 on Vertex AI.

    Args:
        prompt: Description of the motion / action to animate from the image.
        image_gcs_uri: Google Cloud Storage URI of the source image (e.g. gs://bucket/path/img.jpg).
        sample_count: Number of video samples to generate (1-4).
        resolution: Output resolution, e.g. "720p" or "1080p".
    """
    if not OUTPUT_GCS_URI:
        return "Error: VIDEO_OUTPUT_GCS_URI is not set on the server."
    if not image_gcs_uri.startswith("gs://"):
        return "Error: image_gcs_uri must be a gs:// URI."

    try:
        image = types.Image(
            gcs_uri=image_gcs_uri,
            mime_type=_infer_image_mime_type(image_gcs_uri),
        )
        operation = client.models.generate_videos(
            model=VEO_MODEL,
            prompt=prompt,
            image=image,
            config=types.GenerateVideosConfig(
                output_gcs_uri=OUTPUT_GCS_URI,
                number_of_videos=sample_count,
                resolution=resolution,
            ),
        )
        return (
            f"Image-to-video generation started. Operation name: {operation.name}. "
            f"Call fetch_video_result with this name to poll."
        )
    except Exception as e:
        return f"Error triggering image-to-video generation: {str(e)}"


@mcp.tool()
def list_generated_videos(limit: int = 20) -> str:
    """
    Lists previously generated videos in the configured GCS output bucket,
    newest first.

    Args:
        limit: Max number of videos to return (default 20).
    """
    if not OUTPUT_GCS_URI:
        return "Error: VIDEO_OUTPUT_GCS_URI is not set on the server."
    if _storage_client is None:
        return "Error: GOOGLE_CLOUD_PROJECT is not set on the server."

    try:
        bucket_name, prefix = _parse_gcs_uri(OUTPUT_GCS_URI)
        blobs = _storage_client.list_blobs(bucket_name, prefix=prefix)
        videos = [
            {
                "uri": f"gs://{bucket_name}/{b.name}",
                "name": b.name.rsplit("/", 1)[-1],
                "size_mb": round((b.size or 0) / 1024 / 1024, 2),
                "created": b.time_created.isoformat() if b.time_created else None,
            }
            for b in blobs
            if b.name.lower().endswith((".mp4", ".mov", ".webm"))
        ]
        videos.sort(key=lambda v: v["created"] or "", reverse=True)
        videos = videos[:limit]

        if not videos:
            return f"No videos found under {OUTPUT_GCS_URI}."

        lines = [f"Found {len(videos)} video(s):"]
        for v in videos:
            try:
                url = _signed_url(v["uri"])
                lines.append(
                    f"- [{v['name']}]({url}) ({v['size_mb']} MB, {v['created']}) — playable for 24h"
                )
            except Exception:
                lines.append(f"- {v['uri']} ({v['size_mb']} MB, {v['created']})")
        return "\n".join(lines)
    except Exception as e:
        return f"Error listing videos: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
