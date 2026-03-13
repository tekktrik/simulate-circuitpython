# SPDX-FileCopyrightText: Copyright (c) 2026 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""Slim and simple version of the CircuitPython Zephyr test infrastructure."""

import subprocess
import sys


class Simualtor:
    """Zephyr OS native sim wrapper."""

    def __init__(self, firmware_filepath: str, flash_filepath: str, timeout: int = 5) -> None:
        """Intialize the simulator."""
        self.simproc: subprocess.Popen | None = None
        self.cmd = [
            firmware_filepath,
            f"--flash={flash_filepath}",
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


def simulate_circuitpython() -> None:
    """Simulate CircuitPython using a simulator."""
    simulator = Simualtor(sys.argv[1], sys.argv[2])
    result = simulator.simulate()
    print(result)


if __name__ == "__main__":
    simulate_circuitpython()
