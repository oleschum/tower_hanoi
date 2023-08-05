# Towers of Hanoi

This is a Python application that demonstrates the classic problem of the Towers of Hanoi using a graphical user interface (GUI).
The Towers of Hanoi is a mathematical puzzle where the objective is to move a stack of disks from one rod to another while following a set of rules.
The application uses the PySide6 library for the GUI and the Matplotlib library for visualization.

![Screenshot](./tower_hanoi.png?raw=true "Screenshot")

## Requirements

- Python 3.x
- PySide6
- Matplotlib

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies by running the following command: ``pip install PySide6 matplotlib``


## Usage

To run the application, execute the following command:

`python main.py`

The application window will open, displaying the initial state of the Towers of Hanoi puzzle. The GUI provides several buttons for controlling the game:

- **Play**: Starts or pauses the automatic playback of moves.
- **Next**: Moves to the next step in the solution.
- **Previous**: Moves to the previous step in the solution.
- **Reset**: Resets the game to the initial state.
- **Number of disk**: Allows you to change the number of disks in the puzzle.

## How It Works

The application uses the `HanoiGame` class to represent the state of the Towers of Hanoi puzzle. The `HanoiGame` class contains methods for solving the puzzle and manipulating the state of the game. The `TowerOfHanoi` class is responsible for creating the GUI and handling user interactions.

The application uses Matplotlib to visualize the state of the puzzle. Each disk is represented by a colored bar, and the rods are represented by vertical lines. The GUI provides buttons for controlling the game and a spin box for changing the number of disks.

## License

This code is released under the [MIT License](LICENSE).
