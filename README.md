# Circuit Simulator

![gif](https://github.com/LoQiseaking69/CircExplorer/blob/main/ASSETS/CircE.gif)

This CircExplorer is an advanced work in progress; user-friendly, circuit design application built using wxPython. It not only allows users to create, save, and load intricate circuit diagrams but also integrates with the Octopart API for real-time electronic component details. The application leverages SQLite for robust database operations and Matplotlib for sophisticated rendering of circuit diagrams, making it an ideal tool for both hobbyists and professional electronic designers.

## Installation

To get started with Circuit Simulator, ensure you have Python 3 and pip installed on your system.

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Dependencies

Install all required dependencies with the following command:

```bash
pip install -r requirements.txt
```

This will install libraries such as wxPython, Matplotlib, aiohttp, and SQLAlchemy, which are crucial for the application's functionality.

## Usage

To launch the application, execute:

```bash
python circuit_simulator.py
```

The GUI will open, presenting options to design, save, and retrieve circuit diagrams. Utilize the Octopart API integration to fetch real-time data for electronic components, enhancing your design accuracy and feasibility.

## Features

- Interactive GUI for intuitive circuit design.
- Real-time fetching of component data from the Octopart API.
- Capability to save and load complex circuit diagrams to/from a SQLite database.
- High-quality circuit diagram rendering with Matplotlib.
- Asynchronous API calls for efficient data retrieval.
- Modular architecture for easy maintenance and scalability.

## Contributing

Contributions to Circuit Simulator are welcome! Whether it's bug fixes, feature additions, or improvements in documentation, your help is appreciated. Please refer to the `CONTRIBUTING.md` file for guidelines.

## License

Circuit Simulator is released under the GNU General Public License v3.0. For more details, see the [license file](https://github.com/LoQiseaking69/CircExplorer/blob/main/LICENSE).