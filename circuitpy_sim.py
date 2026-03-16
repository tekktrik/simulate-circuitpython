# SPDX-FileCopyrightText: Copyright (c) 2026 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""Slim and simple version of the CircuitPython Zephyr test infrastructure."""

import pathlib
import subprocess
import sys


def simulate(firmware_filepath: str, flash_filepath: str, timeout: int = 5) -> str:
    """Simulate using the native sim firmware."""
    firmware_path = pathlib.Path(firmware_filepath).absolute()
    flash_path = pathlib.Path(flash_filepath).absolute()

    cmd = [
        str(firmware_path),
        f"--flash={str(flash_path)}",
        "-rt",
        "-uart_stdinout",
        f"-stop_at={timeout}",
    ]

    simproc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=None,
    )

    if simproc.stdout is None:
        raise RuntimeError("Failed to capture simulator output")

    recording: bool | None = None
    recorded = ""

    while simproc.poll() is None:
        pass

    output: str = simproc.stdout.read().decode()
    for line in output.split("\n"):
        encoded = line.encode()
        if not line:
            continue
        if encoded.strip() == b"\x1b[2K\x1b[0Gcode.py output:" and recording is None:
            recording = True
        elif line.strip() == "Code done running." and recording:
            recording = False
            break
        elif recording:
            recorded += line + "\n"

    return recorded.strip()


def prepare_flash(flash_filepath: str, circuitpy_filepath: str) -> None:
    """Prepare the native sim flash."""
    flash_path = str(pathlib.Path(flash_filepath).absolute())
    circuitpy_abspath = pathlib.Path(circuitpy_filepath).absolute()

    subprocess.run(
        [
            "truncate",
            "-s",
            "2M",
            f"{flash_path}",
        ],
        timeout=5,
        check=True,
    )

    subprocess.run(
        [
            "mformat",
            "-i",
            f"{flash_path}",
            "::",
        ],
        timeout=5,
        check=True,
    )

    mcopy_cmd = [
        "mcopy",
        "-s",
        "-i",
        f"{flash_path}",
    ]

    files = [str(path) for path in circuitpy_abspath.glob("*")]
    mcopy_cmd.extend(files)
    mcopy_cmd.append("::")

    subprocess.run(
        mcopy_cmd,
        timeout=5,
        check=True,
    )


def simulate_circuitpython_cmdline() -> None:
    """Simulate CircuitPython using a simulator."""
    firmware_filepath = sys.argv[1]
    flash_filepath = sys.argv[2]
    result = simulate(firmware_filepath, flash_filepath)
    print(result)


def prepare_flash_cmdline() -> None:
    """PRepare flash for the simulator."""
    flash_filepath = sys.argv[1]
    circuitpy_filepath = sys.argv[2]
    prepare_flash(flash_filepath, circuitpy_filepath)


if __name__ == "__main__":
    simulate_circuitpython_cmdline()
