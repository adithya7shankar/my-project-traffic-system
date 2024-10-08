
# My Computer Vision Traffic System to aid data analytics without compromising popular data.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
This project is designed to mimic a traffic system using computer vision to create unique signatures of vehicles and provide data for analytics. It leverages Python and Docker to create an efficient and scalable solution. The project was built using Windows and VSCode, so the steps may not be 1:1 if you use a different OS. However the usage of docker should mitigate the build issues.
.

## Features
- **Dockerized Environment:** Easy containerization and deployment with the provided Dockerfile.
- **Cryptographic Operations:** Secure data handling using the cryptography library.
- **Data Visualization:** Advanced plotting and visualization with matplotlib.
- **Modular Design:** Reusable utility functions provided in the `utils.py` module.

## Main Modules

### Data Generation and Processing:
- **generate_vehicle_data(num_vehicles):** Simulates vehicle data generation, including details like speed, size, and device ID.
- **simulate_sensor_data_processing(vehicle_data):** Processes the generated vehicle data, including encryption and anonymization.
- **simulate_data_analysis(encrypted_data_stream):** Analyzes the processed and encrypted vehicle data by decrypting it.

### Cryptographic Operations:
- **generate_signature(device_id):** Generates a unique signature for a device using a hash of the device ID.
- **encrypt_data(data):** Encrypts the provided data string.
- **decrypt_data(encrypted_data):** Decrypts the provided encrypted data.

### Visualization:
- **visualize_speed_distribution(analyzed_data):** Creates a histogram to visualize the distribution of vehicle speeds.

### Vehicle Detection and Video Processing (if applicable):
- **mock_vehicle_detection(frame):** Simulates vehicle detection in a video frame.
- **process_video_feed(video_path):** Simulates the processing of a video feed to extract and anonymize vehicle data.

### Main Execution:
- **main():** The main entry point of the project, orchestrating data generation, processing, analysis, and visualization.
- **run_simulation(iterations, num_vehicles_per_iteration):** Runs multiple iterations of the vehicle data simulation, processing, and analysis.

These modules together form the core functionality of your project, allowing for the generation, processing, encryption, analysis, and visualization of vehicle-related data in a traffic system simulation.


## Installation

### Prerequisites
- Docker installed on your system.
- Python 3.x (if running outside of Docker).

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/adithya7shankar/my-project-traffic-system.git
    ```
2. Create a workspace that looks like this:
    ```sh
    - requirements.txt
    - main.py
    - Dockerfile
    - utils.py
    ```
     
3. Build the Docker image using devcontainers:
    ```sh
    Run it by using devcontainers. 
    -> CTRL+Shift+P or CMD+Shift+P  
    -> Type "Remote-Containers: Reopen in Container"
    -> Now copy the devcontainer.json from the repo and paste it into your devcontainer.json; this will add the extensions in vscode to aid development.
    ```
4. Run the Docker container:
    ```sh
    Run it by using devcontainers. 
    To build your project, simply run the relevant commands within the VS Code terminal, which is now connected to the DevContainer.
    ```

## Usage
To run the main script inside the Docker container:
    ```sh
    python main.py
    ```

### Main Script (`main.py`)
The `main.py` script serves as the entry point to the project, utilizing utility functions from `utils.py` to perform the main tasks.

### Utility Functions (`utils.py`)
This module contains helper functions that support the main script. You can modify or extend these functions to suit your project's needs.

## Configuration
Configurations can be adjusted in the `main.py` script or within Docker. For more complex setups, consider using environment variables or configuration files.

## Contributing
Every project has room for improvement, and this one is no exception. If you'd like to contribute, here’s how you can get involved:

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. Make your changes.
4. Commit your changes:
    ```sh
    git commit -m 'Add your message here'
    ```
5. Push to the branch:
    ```sh
    git push origin feature/your-feature-name
    ```
6. Create a pull request.


## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Created by Adithya Shankar - feel free to contact me at [adithya7shankar@gmail.com](mailto:adithya7shankar@gmail.com).
