# simulate-circuitpython
Simulate CircuitPython using Zephyr simulator

## Inputs

| Argument Name | Description | Default | Notes |
| --- | --- | --- | --- |
| ``version`` | Version of CircuitPython to simulate | ``main`` | Must be a version that supports the Zephyr OS native sim |
| ``circuitpy`` | Filepath to file or folder of files to add to the simualted CIRCUITPY | N/A (required) |  |
| ``circuitpython-folder`` | Folder name to use for the CircuitPython checkout | ``cpysim`` | Change this if it conflicts with another file/folder |

## Outputs

| Argument Name | Description | Notes |
| --- | --- | --- |
| ``output-text`` | The text output from the simulator |  |

## License

This library is available under an MIT license.
