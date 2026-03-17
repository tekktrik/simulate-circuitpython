# simulate-circuitpython-nativesim

Simulate CircuitPython using Zephyr simulator

## prepare-system

Prepare the runner for the simulator (and possible build process)

### Inputs

None

### Outputs

None

## build-firmware

Build the nativesim firmware (or use a cached version if available)

### Inputs

| Argument Name | Description | Default | Notes |
| --- | --- | --- | --- |
| ``version`` | Version of CircuitPython to simulate | ``latest`` | Must be a version that supports the Zephyr OS native sim |
| ``circuitpython-folder`` | Folder name to use for the CircuitPython checkout | ``cpysim`` | Change this if it conflicts with another file/folder |
| ``firmware-filepath`` | Filepath for the built firmware | ``./firmware.exe`` |  |

### Outputs

| Argument Name | Description | Notes |
| --- | --- | --- |
| ``restored`` | Whether the firmware was restored from cache |  |

## prepare-flash

Prepare the flash space for the simulator

### Inputs

| Argument Name | Description | Default | Notes |
| --- | --- | --- | --- |
| ``flash-filepath`` | Filepath for the desired flash binary file | ``./flash.bin`` |  |
| ``circuitpy`` | Filepath to file or folder of files to add to the simualted CIRCUITPY | N/A (required) |  |

### Outputs

None

## simulate

Run the simulator

### Inputs

| Argument Name | Description | Default | Notes |
| --- | --- | --- | --- |
| ``firmware-filepath`` | Filepath for the built firmware | ``./firmware.exe`` |  |
| ``flash-filepath`` | Filepath for the desired flash binary file | ``./flash.bin`` |  |

### Outputs

| Argument Name | Description | Notes |
| --- | --- | --- |
| ``output-text`` | The text output from the simulator |  |

## License

This library is available under an MIT license.
