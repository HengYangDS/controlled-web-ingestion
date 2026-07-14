"""Verify the local Firecrawl image set against reviewed provenance."""

from __future__ import annotations

from typing import Any


def verify_image_records(provenance: dict[str, Any], images: list[dict[str, Any]]) -> list[str]:
    """Return deterministic errors for tag, platform, or local-ID drift."""
    expected_platform = provenance.get("platform")
    if expected_platform != "linux/arm64":
        return ["platform must be linux/arm64"]
    by_tag = {
        tag: image
        for image in images
        if isinstance(image, dict)
        for tag in image.get("RepoTags", [])
        if isinstance(tag, str)
    }
    errors: list[str] = []
    provenance_images = provenance.get("images")
    if not isinstance(provenance_images, dict):
        return ["provenance images must be an object"]
    for name, expected in sorted(provenance_images.items()):
        if not isinstance(expected, dict):
            errors.append(f"{name}: invalid provenance entry")
            continue
        reference = expected.get("reference")
        local_id = expected.get("local_image_id")
        if not isinstance(reference, str) or not isinstance(local_id, str):
            errors.append(f"{name}: reference and local_image_id are required")
            continue
        actual = by_tag.get(reference)
        if actual is None:
            errors.append(f"{name}: missing image tag {reference}")
            continue
        if actual.get("Os") != "linux" or actual.get("Architecture") != "arm64":
            errors.append(f"{name}: architecture must be linux/arm64")
        if actual.get("Id") != local_id:
            errors.append(f"{name}: image_id does not match reviewed local image identity")
    return errors
