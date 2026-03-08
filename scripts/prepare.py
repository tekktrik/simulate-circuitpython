# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
# SPDX-License-Identifier: MIT

"""Prepare the CIRCUITPY drive."""

import sys
import pathlib
import shutil


def prepare():
    src = pathlib.Path(sys.argv[1])
    dst = pathlib.Path(sys.argv[2])

    if not src.exists():
        print(f"Filepath {src.absolute()} does not exist")
        sys.exit(1)

    circuitpy = dst / "CIRCUITPY"
    circuitpy.mkdir()

    if src.is_file():
        print(f"Copying file {src} to {circuitpy}")
        shutil.copy(src, circuitpy)
    else:
        print(f"Copying folder {src} to {circuitpy}")
        shutil.copytree(src, circuitpy, dirs_exist_ok=True)


if __name__ == "__main__":
    prepare()
