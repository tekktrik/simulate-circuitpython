# SPDX-FileCopyrightText: Copyright (c) 2026 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""Slim and simple version of the CircuitPython Zephyr test infrastructure."""

import subprocess


class Simualtor:
    def __init__(self, timeout: int = 5) -> None:
        self.simproc: subprocess.Popen | None = None
        # self.reader = serial.Serial | None = None
        # self.readproc = subprocess.Popen | None = None
        self.cmd = [
            "build-native_native_sim/firmware.exe",
            "--flash=build-native_native_sim/flash.bin",
            "-rt",
            "-uart_stdinout",
            f"-stop_at={timeout}",
        ]

    def simulate(self) -> str:
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

        result = recorded.strip()

        print(result)

        return result


if __name__ == "__main__":
    simulator = Simualtor()
    simulator.simulate()
