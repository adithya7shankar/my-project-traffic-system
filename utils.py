import hashlib
import os
from cryptography.fernet import Fernet
import time
import random
import matplotlib.pyplot as plt
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Generate encryption key and save it (in a real application, store this securely)
def get_or_create_key():
    """Get an existing key or create a new one if it doesn't exist."""
    key_file = "encryption_key.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        return key

# Get or create encryption key
encryption_key = get_or_create_key()
cipher = Fernet(encryption_key)

def generate_signature(device_id: str) -> str:
    """Create a hash of the device_id to generate a unique signature."""
    salt = os.urandom(16)  # Adding randomness to the hash
    signature = hashlib.pbkdf2_hmac('sha256', device_id.encode(), salt, 100000)
    return signature.hex()

def encrypt_data(data: str) -> bytes:
    """Encrypt the provided data string."""
    try:
        encrypted_data = cipher.encrypt(data.encode())
        return encrypted_data
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise

def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypt the provided encrypted data."""
    try:
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        return decrypted_data
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise

def process_data_in_real_time(data_stream):
    """Simulate real-time data processing by generating signatures, anonymizing, and encrypting data."""
    processed_stream = []
    for data in data_stream:
        signature = generate_signature(data['device_id'])
        anonymized_data = {
            'signature': signature,
            'speed': data['speed'],
            'size': data['size'],
        }
        encrypted_data = encrypt_data(str(anonymized_data))
        processed_stream.append(encrypted_data)
        logger.info(f"Processed data for device: {data['device_id']}")
        time.sleep(0.1)  # Reduced delay for faster processing
    return processed_stream

def analyze_traffic_data(encrypted_data_stream):
    """Analyze a stream of encrypted data by decrypting and processing it."""
    analyzed_data = []
    for encrypted_data in encrypted_data_stream:
        decrypted_data = decrypt_data(encrypted_data)
        analyzed_data.append(decrypted_data)
        logger.debug(f"Analyzed data: {decrypted_data}")
    return analyzed_data

def generate_vehicle_data(num_vehicles):
    """Simulate vehicle data generation for a given number of vehicles."""
    vehicle_data = []
    for i in range(num_vehicles):
        device_id = f"vehicle_{i+1}"
        speed = random.randint(30, 70)  # Random speed between 30-70 mph
        size = random.choice(['compact', 'sedan', 'SUV', 'truck'])
        vehicle_data.append({'device_id': device_id, 'speed': f'{speed}mph', 'size': size})
    return vehicle_data

def simulate_sensor_data_processing(vehicle_data):
    """Simulate the processing of sensor data including encryption."""
    return process_data_in_real_time(vehicle_data)

def simulate_data_analysis(encrypted_data_stream):
    """Simulate the analysis of encrypted data by decrypting it."""
    analyzed_data = []
    for encrypted_data in encrypted_data_stream:
        decrypted_data = decrypt_data(encrypted_data)
        analyzed_data.append(decrypted_data)
        logger.info(f"Analyzed data successfully")
        logger.debug(f"Data details: {decrypted_data}")
    return analyzed_data

def extract_speed(data_str):
    """Extract speed value from the data string."""
    try:
        # Handle different string formats that might be in the analyzed data
        if "'speed':" in data_str:
            speed_part = data_str.split("'speed':")[1].split(",")[0].strip()
            speed_str = speed_part.replace("'", "").replace('"', '')
            return int(speed_str.rstrip('mph'))
        else:
            # For alternative format
            speed_part = data_str.split("speed=")[1].split(",")[0].strip()
            return int(speed_part.rstrip('mph'))
    except Exception as e:
        logger.error(f"Error extracting speed: {e} from data: {data_str}")
        return 0  # Return default value if extraction fails

def visualize_speed_distribution(analyzed_data):
    """Visualize the distribution of vehicle speeds using a histogram."""
    try:
        speeds = [extract_speed(data) for data in analyzed_data]
        
        plt.figure(figsize=(10, 6))
        plt.hist(speeds, bins=range(30, 75, 5), edgecolor='black')
        plt.title('Vehicle Speed Distribution')
        plt.xlabel('Speed (mph)')
        plt.ylabel('Number of Vehicles')
        
        # Save the figure for headless environments (useful in Docker)
        plt.savefig('speed_distribution.png')
        logger.info("Speed distribution visualization saved to speed_distribution.png")
        
        # Try to display it if possible
        try:
            plt.show()
        except Exception as e:
            logger.warning(f"Could not display plot: {e}")
        
    except Exception as e:
        logger.error(f"Error in visualization: {e}")

def run_simulation(iterations, num_vehicles_per_iteration):
    """Run multiple iterations of the vehicle data simulation, processing, and analysis."""
    all_analyzed_data = []
    
    for i in range(iterations):
        logger.info(f"\n--- Simulation Iteration {i+1} ---")
        vehicle_data = generate_vehicle_data(num_vehicles_per_iteration)
        processed_data = simulate_sensor_data_processing(vehicle_data)
        analyzed_data = simulate_data_analysis(processed_data)
        all_analyzed_data.extend(analyzed_data)
    
    # Visualize combined results
    visualize_speed_distribution(all_analyzed_data)
    return all_analyzed_data

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_simulation(iterations=3, num_vehicles_per_iteration=10)
