# Computer Vision Traffic System for Privacy-Preserving Analytics

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Docker Setup](#docker-setup)
  - [Local Setup](#local-setup)
- [Usage](#usage)
  - [Running with Docker](#running-with-docker)
  - [Running Locally](#running-locally)
  - [Running Tests](#running-tests)
  - [Configuration Options](#configuration-options)
- [Core Modules](#core-modules)
- [Development](#development)
  - [File Structure](#file-structure)
  - [Development with VS Code DevContainers](#development-with-vs-code-devcontainers)
- [Security & Privacy](#security--privacy)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
This project simulates a traffic monitoring system using computer vision techniques to generate and analyze vehicle data while preserving privacy. The system creates unique cryptographic signatures for vehicles, processes the data securely, and provides analytics without compromising individual privacy. It's implemented as a fully containerized solution using Docker for easy deployment and scalability.

## Features
- **Privacy-Preserving Analytics**: Uses cryptographic signatures instead of identifiable information
- **Dockerized Environment**: Easy containerization and deployment with an optimized Dockerfile
- **Secure Cryptography**: Data encryption and decryption using Fernet symmetric encryption
- **Enhanced Data Visualization**: Multiple visualization types including speed histograms and vehicle size distributions
- **Modular Architecture**: Well-structured code with separation of concerns
- **Comprehensive Logging**: Detailed logging system for troubleshooting and auditing
- **Simulation Capabilities**: Run single or multi-iteration traffic simulations
- **Unit Testing**: Comprehensive test suite to ensure code quality and reliability
- **Type Hints**: Improved code readability and IDE support with Python type annotations

## System Architecture
The system follows a modular design with these main components:

1. **Data Generation**: Simulates vehicle detection and data collection
2. **Data Processing**: Anonymizes and encrypts sensitive vehicle information
3. **Data Analysis**: Decrypts and analyzes the processed data
4. **Visualization**: Creates graphical representations of traffic patterns

## Installation

### Prerequisites
- Docker and Docker Compose (for containerized deployment)
- Python 3.9+ (for local development)
- Git

### Docker Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/adithya7shankar/traffic-system.git
   cd traffic-system
   ```

2. Build and run with Docker:
   ```sh
   docker build -t traffic-system .
   docker run -p 80:80 traffic-system
   ```

3. Access the output visualizations:
   ```sh
   # Mount volumes for persistent output and logs
   docker run -p 80:80 -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs traffic-system
   ```

### Local Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/adithya7shankar/traffic-system.git
   cd traffic-system
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Running with Docker
```sh
# Run the default simulation
docker run -p 80:80 traffic-system

# Run with mounted volumes for output visualization and logs
docker run -p 80:80 -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs traffic-system
```

### Running Locally
```sh
# Run the default simulation
python main.py

# Run with custom parameters
python -c "from utils import run_simulation; run_simulation(iterations=5, num_vehicles_per_iteration=30)"
```

### Running Tests
```sh
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=. --cov-report=term-missing

# Run a specific test file
pytest test_utils.py
```

### Configuration Options
The system can be configured by modifying parameters in the `main.py` file:

- `num_vehicles`: Number of vehicles to simulate in a single run
- `iterations`: Number of simulation iterations to run
- `num_vehicles_per_iteration`: Number of vehicles per iteration
- `processing_delay`: Adjust the simulated processing delay (in seconds)

## Core Modules

### Data Generation and Processing
- **generate_vehicle_data(num_vehicles)**: Creates simulated vehicle data with speed, size, and device ID
- **simulate_sensor_data_processing(vehicle_data)**: Processes and encrypts the vehicle data
- **simulate_data_analysis(encrypted_data)**: Decrypts and analyzes the processed data

### Cryptographic Operations
- **generate_signature(device_id)**: Creates a unique vehicle signature using cryptographic hashing
- **encrypt_data(data)**: Securely encrypts data using Fernet symmetric encryption
- **decrypt_data(encrypted_data)**: Decrypts the encrypted data for analysis

### Visualization
- **visualize_speed_distribution(analyzed_data)**: Creates histograms of vehicle speed distributions
- **visualize_vehicle_sizes(analyzed_data)**: Creates pie charts of vehicle size distributions
- **Output**: Visualization results are saved to PNG files in the output directory

## Development

### File Structure
```
traffic-system/
├── Dockerfile             # Optimized container definition
├── README.md              # This documentation
├── .gitignore             # Git ignore configuration
├── main.py                # Main application entry point
├── requirements.txt       # Python dependencies
├── test_utils.py          # Unit tests for utility functions
├── utils.py               # Core utility functions
├── logs/                  # Generated log files
└── output/                # Generated visualizations
```

### Development with VS Code DevContainers
1. Open the project in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Select "Remote-Containers: Reopen in Container"
4. When the container is built and running, you can develop within it

## Security & Privacy
This system implements several security and privacy measures:

- **Data Anonymization**: Vehicle IDs are converted to cryptographic signatures
- **Encryption**: All processed data is encrypted using Fernet symmetric encryption
- **Key Management**: Encryption keys are generated and stored securely
- **No Persistent Identifiers**: The system avoids storing any personally identifiable information
- **Error Handling**: Improved error handling for cryptographic operations
- **Secure File Operations**: Better handling of file operations with proper error handling

## Contributing
Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch:
   ```sh
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m 'Add some feature'
   ```
4. Push to your branch:
   ```sh
   git push origin feature/your-feature-name
   ```
5. Open a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
Created by Adithya Shankar - feel free to contact me at [adithya7shankar@gmail.com](mailto:adithya7shankar@gmail.com).
