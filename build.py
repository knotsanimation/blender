import logging
import os
import sys

import rezbuild_utils


LOGGER = logging.getLogger(__name__)


def build():
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

    rezbuild_utils.download_and_install_build(
        blender_url,
        extract_reference_file_name="blender.exe",
        use_cache=True,
    )

    LOGGER.info("finished")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname: <7} | {asctime} [{name}] {message}",
        style="{",
        stream=sys.stdout,
    )
    build()
