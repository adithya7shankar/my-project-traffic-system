import hashlib
import os
from cryptography.fernet import Fernet
import time
import random
import matplotlib.pyplot as plt

# Generate encryption key (do this once and store it securely)
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

def generate_signature(device_id: str) -> str:
    """Create a hash of the device_id to generate a unique signature."""
    salt = os.urandom(16)  # Adding randomness to the hash
    signature = hashlib.pbkdf2_hmac('sha256', device_id.encode(), salt, 100000)
    return signature.hex()

def encrypt_data(data: str) -> str:
    """Encrypt the provided data string."""
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypt the provided encrypted data."""
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

def process_data_in_real_time(data_stream):
    """Simulate real-time data processing by generating signatures, anonymizing, and encrypting data."""
    for data in data_stream:
        signature = generate_signature(data['device_id'])
        anonymized_data = {
            'signature': signature,
            'speed': data['speed'],
            'size': data['size'],
        }
        encrypted_data = encrypt_data(str(anonymized_data))
        print(f"Processed and Encrypted Data: {encrypted_data}")
        time.sleep(1)  # Simulate real-time processing delay

def analyze_traffic_data(encrypted_data_stream):
    """Analyze a stream of encrypted data by decrypting and printing it."""
    for encrypted_data in encrypted_data_stream:
        decrypted_data = decrypt_data(encrypted_data)
        print(f"Decrypted and Analyzed Data: {decrypted_data}")

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
    processed_data_stream = []
    for data in vehicle_data:
        signature = generate_signature(data['device_id'])
        anonymized_data = {
            'signature': signature,
            'speed': data['speed'],
            'size': data['size'],
        }
        encrypted_data = encrypt_data(str(anonymized_data))
        processed_data_stream.append(encrypted_data)
        time.sleep(0.5)  # Simulate processing delay
    return processed_data_stream

def simulate_data_analysis(encrypted_data_stream):
    """Simulate the analysis of encrypted data by decrypting it."""
    analyzed_data = []
    for encrypted_data in encrypted_data_stream:
        decrypted_data = decrypt_data(encrypted_data)
        analyzed_data.append(decrypted_data)
        print(f"Analyzed Decrypted Data: {decrypted_data}")
    return analyzed_data

def visualize_speed_distribution(analyzed_data):
    """Visualize the distribution of vehicle speeds using a histogram."""
    speeds = [int(data.split(",")[1].split("=")[1][:-3]) for data in analyzed_data]
    plt.hist(speeds, bins=range(30, 75, 5), edgecolor='black')
    plt.title('Vehicle Speed Distribution')
    plt.xlabel('Speed (mph)')
    plt.ylabel('Number of Vehicles')
    plt.show()

def run_simulation(iterations, num_vehicles_per_iteration):
    """Run multiple iterations of the vehicle data simulation, processing, and analysis."""
    for i in range(iterations):
        print(f"\n--- Simulation Iteration {i+1} ---")
        vehicle_data = generate_vehicle_data(num_vehicles_per_iteration)
        processed_data = simulate_sensor_data_processing(vehicle_data)
        analyzed_data = simulate_data_analysis(processed_data)
        visualize_speed_distribution(analyzed_data)

# Example usage
if __name__ == "__main__":
    run_simulation(iterations=3, num_vehicles_per_iteration=10)
