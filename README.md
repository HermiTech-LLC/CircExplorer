# Circuit Simulator

![gif](https://github.com/LoQiseaking69/CircExplorer/blob/main/ASSETS/CircE.gif)

This application is a circuit renderer, built using wxPython. It features the capability to save and load circuit diagrams, integrate with the Octopart API for component details, and demonstrates integration with SQLite for database operations and matplotlib for rendering circuit diagrams.

## Installation

To run this application, you need to install the necessary dependencies.

### Prerequisites

- Python 3
- pip

### Dependencies

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes the following libraries:

- wxPython
- matplotlib
- requests

## Usage

Run the script `circuit_simulator.py` to start the application:

```bash
python circuit_simulator.py
```

Upon running the application, you can create, save, and load circuit diagrams. The integration with the Octopart API allows for fetching detailed component information to enhance the circuit design process.

## Features

- Sophisticated circuit diagram rendering with matplotlib.
- Saving and loading circuit diagrams using SQLite.
- Integration with the Octopart API for detailed electronic component information.
- Advanced circuit design capabilities based on user input and component specifications.

## License

This project is open-source and available under the GNU v3 License seen [here](https://github.com/LoQiseaking69/CircExplorer/blob/main/LICENSE).