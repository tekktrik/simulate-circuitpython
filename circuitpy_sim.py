# SPDX-FileCopyrightText: Copyright (c) 2026 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""Slim and simple version of the CircuitPython Zephyr test infrastructure."""

import pathlib
import subprocess
import sys


class Simualtor:
    """Zephyr OS native sim wrapper."""

    def __init__(self, firmware_filepath: str, flash_filepath: str, timeout: int = 5) -> None:
        """Intialize the simulator."""
        self.firmware_path = pathlib.Path(firmware_filepath).absolute()
        self.flash_path = pathlib.Path(flash_filepath).absolute()
        self.simproc: subprocess.Popen | None = None
        self.cmd = [
            str(self.firmware_path),
            f"--flash={str(self.flash_path)}",
            "-rt",
            "-uart_stdinout",
            f"-stop_at={timeout}",
        ]

    def simulate(self) -> str:
        """Simulate using the native sim firmware."""
        self.simproc = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
        )

        if self.simproc.stdout is None:
            raise RuntimeError("Failed to capture simulator output")

        recording: bool | None = None
        recorded = ""

        while self.simproc.poll() is None:
            pass

        output: str = self.simproc.stdout.read().decode()
        for line in output.split("\n"):
            encoded = line.encode()
            if not line:
                continue
            if (
                encoded.strip() == b"\x1b[2K\x1b[0Gcode.py output:"
                and recording is None
            ):
                recording = True
            elif line.strip() == "Code done running." and recording:
                recording = False
                break
            elif recording:
                recorded += line + "\n"

        return recorded.strip()
    
    @classmethod
    def prepare_flash(cls, flash_filepath: str, circuitpy_filepath: str) -> None:
        """Prepare the native sim flash."""
        flash_path = str(pathlib.Path(flash_filepath).absolute())
        circuitpy_abspath = pathlib.Path(circuitpy_filepath).absolute()

        subprocess.run(
            [
                "truncate",
                "-s",
                "2M",
                f"{ flash_path }",
            ],
            timeout=5,
            check=True,
        )

        subprocess.run(
            [
                "mformat",
                "-i",
                f"{ flash_path }",
                "::",
            ],
            timeout=5,
            check=True,
        )

        mcopy_cmd = [
            "mcopy",
            "-s",
            "-i",
            f"{ flash_path }",
        ]

        files = [str(path) for path in circuitpy_abspath.glob("*")]
        mcopy_cmd.extend(files)
        mcopy_cmd.append("::")
        
        subprocess.run(
            mcopy_cmd,
            timeout=5,
            check=True,
        )


def simulate_circuitpython() -> None:
    """Simulate CircuitPython using a simulator."""
    simulator = Simualtor(sys.argv[1], sys.argv[2])
    result = simulator.simulate()
    print(result)


def prepare_flash() -> None:
    """PRepare flash for the simulator."""
    flash_filepath = sys.argv[1]
    circuitpy_filepath = sys.argv[2]
    Simualtor.prepare_flash(flash_filepath, circuitpy_filepath)


if __name__ == "__main__":
    simulate_circuitpython()
