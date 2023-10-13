import logging
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import rezbuild_utils


LOGGER = logging.getLogger(__name__)


def extract(downloaded_file: Path):
    extract_root = downloaded_file.parent
    LOGGER.info(f"extracting {downloaded_file.name} to {extract_root}...")
    with zipfile.ZipFile(downloaded_file, "r") as zip_file:
        zip_file.extractall(extract_root)
    downloaded_file.unlink()

    LOGGER.info(f"moving extracted file to proper location ...")
    blender_exe = list(extract_root.glob("**/blender.exe"))[0]
    for file in blender_exe.parent.glob("*"):
        file.rename(extract_root / file.name)


def _build(temp_folder: Path):
    """
    We download blender in a local temp folder for faster speed.
    """
    blender_version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    blender_version_split = blender_version.split(".")
    # XXX: we add an additional sub-patch token for rez versioning
    #   so it need to be removed to get an official blender version
    blender_version = ".".join(blender_version_split[:-1])

    platform = os.environ["REZ_PLATFORM_VERSION"]
    # key=rez, values=blender
    platform_map = {
        "windows": "windows-x64.zip",
        "linux": "linux-x64.tar.xz",
        # missing for arch=arm64
        "osx": "macos-x64.dmg",
    }
    blender_filename = f"blender-{blender_version}-{platform_map[platform]}"

    blender_url = "https://download.blender.org/release/Blender"
    blender_url += f"{blender_version_split[0]}.{blender_version_split[1]}"
    blender_url += f"/{blender_filename}"

    blender_root_dir = temp_folder
    blender_download_file_local = blender_root_dir / blender_filename
    LOGGER.info(f"downloading {blender_url} ...")
    rezbuild_utils.download_file(
        blender_url,
        blender_download_file_local,
        use_cache=True,
    )

    target_dir = Path(os.environ["REZ_BUILD_INSTALL_PATH"])
    LOGGER.info(f"copying {blender_download_file_local.name} to {target_dir} ...")
    shutil.copy2(blender_download_file_local, target_dir)
    blender_download_file_build = target_dir / blender_download_file_local.name

    extract(blender_download_file_build)

    LOGGER.info("finished")


def build():
    prefix = f"{os.environ['REZ_BUILD_PROJECT_NAME']}-{os.environ['REZ_BUILD_PROJECT_VERSION']}-"
    temp_folder = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        _build(temp_folder)
    except Exception as error:
        # XXX: hack as progress bar doesn't add a new line if not finished
        print("")
        raise
    finally:
        LOGGER.info(f"removing temporary directory {temp_folder}")
        shutil.rmtree(temp_folder)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    build()
