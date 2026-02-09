"""Unit tests for ImageExtractor (tar extraction only, no Docker)."""

import pytest
import tempfile
import tarfile
from pathlib import Path
from netsec_container.core.image_extractor import ImageExtractor


@pytest.mark.unit
def test_image_extractor_init():
    """ImageExtractor initializes."""
    ext = ImageExtractor()
    assert ext is not None
    assert ext.name == "Image Extractor"
    assert isinstance(ext.use_docker, bool)
    assert isinstance(ext.use_podman, bool)
    assert isinstance(ext.use_skopeo, bool)
    assert isinstance(ext.use_crane, bool)


@pytest.mark.unit
def test_extract_tar_file_minimal():
    """extract_tar_file extracts a minimal tar to a directory."""
    ext = ImageExtractor()
    with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as f:
        tar_path = Path(f.name)
    try:
        with tarfile.open(tar_path, "w") as tar:
            # Add a dummy member
            import io
            data = io.BytesIO(b"test")
            info = tarfile.TarInfo(name="layer/file.txt")
            info.size = 4
            tar.addfile(info, data)
        out = ext.extract_tar_file(tar_path)
        assert out is not None
        assert out.exists()
        assert out.is_dir()
        extracted_file = out / "layer" / "file.txt"
        assert extracted_file.exists()
        assert extracted_file.read_bytes() == b"test"
    finally:
        tar_path.unlink(missing_ok=True)
