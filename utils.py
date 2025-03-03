import hashlib
import os
import json
from typing import Dict, List, Union, Any, Optional
from cryptography.fernet import Fernet
import time
import random
import matplotlib.pyplot as plt
import logging
from pathlib import Path

# Initialize logger
logger = logging.getLogger(__name__)

# Create output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Generate encryption key and save it (in a real application, store this securely)
def get_or_create_key() -> bytes:
    """
    Get an existing key or create a new one if it doesn't exist.
    
    In a production environment, this key should be stored in a secure key management system,
    not in a local file.
    
    Returns:
        bytes: The encryption key
    """
    key_file = OUTPUT_DIR / "encryption_key.key"
    try:
        if key_file.exists():
            with open(key_file, "rb") as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as file:
                file.write(key)
            logger.info(f"Created new encryption key at {key_file}")
            return key
    except Exception as e:
        logger.error(f"Error accessing encryption key: {e}")
        # Fallback to in-memory key if file operations fail
        logger.warning("Using temporary in-memory encryption key")
        return Fernet.generate_key()

# Get or create encryption key
encryption_key = get_or_create_key()
cipher = Fernet(encryption_key)

def generate_signature(device_id: str) -> str:
    """
    Create a hash of the device_id to generate a unique signature.
    
    Args:
        device_id (str): The device identifier to hash
        
    Returns:
        str: A hexadecimal representation of the signature
    """
    # Use a consistent salt for the same device_id to get the same signature
    # In a real system, this would use a secure, stored salt
    salt = hashlib.sha256(device_id.encode()).digest()[:16]
    signature = hashlib.pbkdf2_hmac('sha256', device_id.encode(), salt, 100000)
    return signature.hex()

def encrypt_data(data: Union[str, Dict, List]) -> bytes:
    """
    Encrypt the provided data.
    
    Args:
        data (Union[str, Dict, List]): Data to encrypt, can be a string or JSON-serializable object
        
    Returns:
        bytes: Encrypted data
        
    Raises:
        ValueError: If encryption fails
    """
    try:
        # Convert dict/list to JSON string if needed
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        
        encrypted_data = cipher.encrypt(data.encode())
        return encrypted_data
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise ValueError(f"Failed to encrypt data: {e}")

def decrypt_data(encrypted_data: bytes) -> Dict[str, Any]:
    """
    Decrypt the provided encrypted data.
    
    Args:
        encrypted_data (bytes): The encrypted data to decrypt
        
    Returns:
        Dict[str, Any]: Decrypted data as a dictionary
        
    Raises:
        ValueError: If decryption or JSON parsing fails
    """
    try:
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        # Try to parse as JSON
        try:
            return json.loads(decrypted_data)
        except json.JSONDecodeError:
            # If not valid JSON, return as string in a dict
            return {"data": decrypted_data}
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise ValueError(f"Failed to decrypt data: {e}")

def process_data_in_real_time(data_stream: List[Dict[str, Any]], 
                             processing_delay: float = 0.05) -> List[bytes]:
    """
    Simulate real-time data processing by generating signatures, anonymizing, and encrypting data.
    
    Args:
        data_stream (List[Dict[str, Any]]): List of vehicle data dictionaries
        processing_delay (float, optional): Simulated processing delay in seconds. Defaults to 0.05.
        
    Returns:
        List[bytes]: List of encrypted data
    """
    processed_stream = []
    for data in data_stream:
        signature = generate_signature(data['device_id'])
        anonymized_data = {
            'signature': signature,
            'speed': data['speed'],
            'size': data['size'],
            'timestamp': time.time()
        }
        encrypted_data = encrypt_data(anonymized_data)
        processed_stream.append(encrypted_data)
        logger.info(f"Processed data for device: {data['device_id']}")
        
        # Simulate processing delay (can be adjusted or disabled)
        if processing_delay > 0:
            time.sleep(processing_delay)
            
    return processed_stream

def generate_vehicle_data(num_vehicles: int) -> List[Dict[str, Any]]:
    """
    Simulate vehicle data generation for a given number of vehicles.
    
    Args:
        num_vehicles (int): Number of vehicles to simulate
        
    Returns:
        List[Dict[str, Any]]: List of vehicle data dictionaries
    """
    vehicle_data = []
    for i in range(num_vehicles):
        device_id = f"vehicle_{i+1}"
        speed = random.randint(30, 70)  # Random speed between 30-70 mph
        size = random.choice(['compact', 'sedan', 'SUV', 'truck'])
        vehicle_data.append({
            'device_id': device_id, 
            'speed': speed,  # Store as integer for easier processing
            'size': size
        })
    return vehicle_data

def simulate_sensor_data_processing(vehicle_data: List[Dict[str, Any]]) -> List[bytes]:
    """
    Simulate the processing of sensor data including encryption.
    
    Args:
        vehicle_data (List[Dict[str, Any]]): List of vehicle data dictionaries
        
    Returns:
        List[bytes]: List of encrypted data
    """
    return process_data_in_real_time(vehicle_data)

def simulate_data_analysis(encrypted_data_stream: List[bytes]) -> List[Dict[str, Any]]:
    """
    Simulate the analysis of encrypted data by decrypting it.
    
    Args:
        encrypted_data_stream (List[bytes]): List of encrypted data
        
    Returns:
        List[Dict[str, Any]]: List of decrypted data dictionaries
    """
    analyzed_data = []
    for encrypted_data in encrypted_data_stream:
        try:
            decrypted_data = decrypt_data(encrypted_data)
            analyzed_data.append(decrypted_data)
            logger.info("Analyzed data successfully")
            logger.debug(f"Data details: {decrypted_data}")
        except ValueError as e:
            logger.error(f"Failed to analyze data: {e}")
    
    return analyzed_data

def extract_speed(data: Union[Dict[str, Any], str]) -> int:
    """
    Extract speed value from the data.
    
    Args:
        data (Union[Dict[str, Any], str]): Data to extract speed from
        
    Returns:
        int: Speed value in mph
    """
    try:
        # If data is already a dictionary
        if isinstance(data, dict):
            speed = data.get('speed', 0)
            # Handle string speed values with 'mph' suffix
            if isinstance(speed, str) and 'mph' in speed:
                return int(speed.rstrip('mph'))
            return int(speed)
        
        # If data is a string (legacy support)
        elif isinstance(data, str):
            if "'speed':" in data:
                speed_part = data.split("'speed':")[1].split(",")[0].strip()
                speed_str = speed_part.replace("'", "").replace('"', '')
                return int(speed_str.rstrip('mph') if 'mph' in speed_str else speed_str)
            elif "speed=" in data:
                speed_part = data.split("speed=")[1].split(",")[0].strip()
                return int(speed_part.rstrip('mph') if 'mph' in speed_part else speed_part)
        
        # Default fallback
        return 0
    except Exception as e:
        logger.error(f"Error extracting speed: {e} from data: {data}")
        return 0  # Return default value if extraction fails

def visualize_speed_distribution(analyzed_data: List[Dict[str, Any]]) -> None:
    """
    Visualize the distribution of vehicle speeds using a histogram.
    
    Args:
        analyzed_data (List[Dict[str, Any]]): List of analyzed data dictionaries
    """
    try:
        speeds = [extract_speed(data) for data in analyzed_data]
        
        plt.figure(figsize=(10, 6))
        plt.hist(speeds, bins=range(30, 75, 5), edgecolor='black')
        plt.title('Vehicle Speed Distribution')
        plt.xlabel('Speed (mph)')
        plt.ylabel('Number of Vehicles')
        plt.grid(axis='y', alpha=0.75)
        
        # Save the figure to output directory
        output_file = OUTPUT_DIR / 'speed_distribution.png'
        plt.savefig(output_file)
        logger.info(f"Speed distribution visualization saved to {output_file}")
        
        # Try to display it if possible
        try:
            plt.show()
        except Exception as e:
            logger.warning(f"Could not display plot: {e}")
        
    except Exception as e:
        logger.error(f"Error in visualization: {e}")

def visualize_vehicle_sizes(analyzed_data: List[Dict[str, Any]]) -> None:
    """
    Visualize the distribution of vehicle sizes using a pie chart.
    
    Args:
        analyzed_data (List[Dict[str, Any]]): List of analyzed data dictionaries
    """
    try:
        # Extract vehicle sizes
        sizes = {}
        for data in analyzed_data:
            if isinstance(data, dict) and 'size' in data:
                size = data['size']
                sizes[size] = sizes.get(size, 0) + 1
            elif isinstance(data, str) and "'size':" in data:
                # Legacy string format support
                size_part = data.split("'size':")[1].split(",")[0].strip()
                size = size_part.replace("'", "").replace('"', '')
                sizes[size] = sizes.get(size, 0) + 1
        
        if not sizes:
            logger.warning("No vehicle size data found for visualization")
            return
            
        # Create pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(sizes.values(), labels=sizes.keys(), autopct='%1.1f%%', 
                shadow=True, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Vehicle Size Distribution')
        
        # Save the figure
        output_file = OUTPUT_DIR / 'vehicle_sizes.png'
        plt.savefig(output_file)
        logger.info(f"Vehicle size distribution saved to {output_file}")
        
        # Try to display it if possible
        try:
            plt.show()
        except Exception as e:
            logger.warning(f"Could not display plot: {e}")
            
    except Exception as e:
        logger.error(f"Error in vehicle size visualization: {e}")

def run_simulation(iterations: int, num_vehicles_per_iteration: int) -> List[Dict[str, Any]]:
    """
    Run multiple iterations of the vehicle data simulation, processing, and analysis.
    
    Args:
        iterations (int): Number of simulation iterations
        num_vehicles_per_iteration (int): Number of vehicles per iteration
        
    Returns:
        List[Dict[str, Any]]: Combined analyzed data from all iterations
    """
    all_analyzed_data = []
    
    for i in range(iterations):
        logger.info(f"\n--- Simulation Iteration {i+1}/{iterations} ---")
        vehicle_data = generate_vehicle_data(num_vehicles_per_iteration)
        processed_data = simulate_sensor_data_processing(vehicle_data)
        analyzed_data = simulate_data_analysis(processed_data)
        all_analyzed_data.extend(analyzed_data)
        
        # Log progress
        logger.info(f"Completed iteration {i+1}/{iterations} with {len(analyzed_data)} vehicles processed")
    
    # Visualize combined results
    visualize_speed_distribution(all_analyzed_data)
    visualize_vehicle_sizes(all_analyzed_data)
    
    return all_analyzed_data

# Example usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    run_simulation(iterations=3, num_vehicles_per_iteration=10)
