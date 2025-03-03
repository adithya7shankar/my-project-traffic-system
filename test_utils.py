import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt

from utils import (
    get_or_create_key,
    generate_signature,
    encrypt_data,
    decrypt_data,
    process_data_in_real_time,
    generate_vehicle_data,
    simulate_sensor_data_processing,
    simulate_data_analysis,
    extract_speed,
    visualize_speed_distribution,
    visualize_vehicle_sizes,
    run_simulation
)

# Fixture to create a temporary output directory for tests
@pytest.fixture
def temp_output_dir(monkeypatch, tmp_path):
    """Create a temporary output directory for tests."""
    # Patch the OUTPUT_DIR in utils.py
    monkeypatch.setattr("utils.OUTPUT_DIR", tmp_path)
    return tmp_path

# Test encryption and decryption
def test_encrypt_decrypt_data():
    """Test that data can be encrypted and then decrypted correctly."""
    # Test with a dictionary
    original_data = {"speed": 55, "size": "sedan", "signature": "abc123"}
    encrypted = encrypt_data(original_data)
    decrypted = decrypt_data(encrypted)
    
    assert isinstance(encrypted, bytes)
    assert isinstance(decrypted, dict)
    assert decrypted["speed"] == original_data["speed"]
    assert decrypted["size"] == original_data["size"]
    assert decrypted["signature"] == original_data["signature"]
    
    # Test with a string
    original_string = "test data string"
    encrypted = encrypt_data(original_string)
    decrypted = decrypt_data(encrypted)
    
    assert isinstance(encrypted, bytes)
    assert isinstance(decrypted, dict)
    assert "data" in decrypted or original_string in str(decrypted)

# Test signature generation
def test_generate_signature():
    """Test that signatures are consistent for the same input but unique for different inputs."""
    # Same device_id should generate the same signature
    device_id = "test_device_123"
    sig1 = generate_signature(device_id)
    sig2 = generate_signature(device_id)
    assert sig1 == sig2
    
    # Different device_ids should generate different signatures
    other_device_id = "test_device_456"
    sig3 = generate_signature(other_device_id)
    assert sig1 != sig3

# Test key generation
def test_get_or_create_key(temp_output_dir):
    """Test that an encryption key can be created and retrieved."""
    # First call should create a new key
    key1 = get_or_create_key()
    assert isinstance(key1, bytes)
    
    # Key file should exist
    key_file = temp_output_dir / "encryption_key.key"
    assert key_file.exists()
    
    # Second call should retrieve the same key
    key2 = get_or_create_key()
    assert key1 == key2

# Test vehicle data generation
def test_generate_vehicle_data():
    """Test that vehicle data is generated with the expected structure."""
    num_vehicles = 10
    vehicle_data = generate_vehicle_data(num_vehicles)
    
    assert len(vehicle_data) == num_vehicles
    
    # Check structure of first vehicle
    vehicle = vehicle_data[0]
    assert "device_id" in vehicle
    assert "speed" in vehicle
    assert "size" in vehicle
    
    # Speed should be an integer between 30 and 70
    assert isinstance(vehicle["speed"], int)
    assert 30 <= vehicle["speed"] <= 70
    
    # Size should be one of the expected values
    assert vehicle["size"] in ["compact", "sedan", "SUV", "truck"]

# Test speed extraction
def test_extract_speed():
    """Test that speed can be extracted from different data formats."""
    # Test with dictionary
    data_dict = {"speed": 45, "size": "sedan"}
    assert extract_speed(data_dict) == 45
    
    # Test with string speed value
    data_dict_str_speed = {"speed": "55mph", "size": "SUV"}
    assert extract_speed(data_dict_str_speed) == 55
    
    # Test with string format (legacy support)
    data_str = "{'signature': 'abc123', 'speed': '60mph', 'size': 'truck'}"
    assert extract_speed(data_str) == 60
    
    # Test with alternative string format
    data_str_alt = "signature=xyz789, speed=35mph, size=compact"
    assert extract_speed(data_str_alt) == 35
    
    # Test with invalid data
    assert extract_speed("invalid data") == 0

# Test data processing
@patch("time.sleep")  # Mock sleep to speed up tests
def test_process_data_in_real_time(mock_sleep):
    """Test that vehicle data can be processed in real time."""
    # Create test data
    vehicle_data = [
        {"device_id": "test1", "speed": 50, "size": "sedan"},
        {"device_id": "test2", "speed": 65, "size": "SUV"}
    ]
    
    # Process data
    processed_data = process_data_in_real_time(vehicle_data, processing_delay=0)
    
    assert len(processed_data) == 2
    assert isinstance(processed_data[0], bytes)
    assert isinstance(processed_data[1], bytes)
    
    # Decrypt and verify
    decrypted1 = decrypt_data(processed_data[0])
    assert "signature" in decrypted1
    assert decrypted1["speed"] == 50
    assert decrypted1["size"] == "sedan"
    assert "timestamp" in decrypted1

# Test visualization functions
@patch("matplotlib.pyplot.savefig")
@patch("matplotlib.pyplot.show")
def test_visualize_speed_distribution(mock_show, mock_savefig, temp_output_dir):
    """Test that speed distribution visualization works."""
    # Create test data
    analyzed_data = [
        {"signature": "abc123", "speed": 45, "size": "sedan"},
        {"signature": "def456", "speed": 55, "size": "SUV"},
        {"signature": "ghi789", "speed": 65, "size": "truck"}
    ]
    
    # Call visualization function
    visualize_speed_distribution(analyzed_data)
    
    # Check that savefig was called
    mock_savefig.assert_called_once()
    mock_show.assert_called_once()

@patch("matplotlib.pyplot.savefig")
@patch("matplotlib.pyplot.show")
def test_visualize_vehicle_sizes(mock_show, mock_savefig, temp_output_dir):
    """Test that vehicle size visualization works."""
    # Create test data
    analyzed_data = [
        {"signature": "abc123", "speed": 45, "size": "sedan"},
        {"signature": "def456", "speed": 55, "size": "SUV"},
        {"signature": "ghi789", "speed": 65, "size": "truck"},
        {"signature": "jkl012", "speed": 50, "size": "sedan"}
    ]
    
    # Call visualization function
    visualize_vehicle_sizes(analyzed_data)
    
    # Check that savefig was called
    mock_savefig.assert_called_once()
    mock_show.assert_called_once()

# Test the full simulation
@patch("utils.visualize_speed_distribution")
@patch("utils.visualize_vehicle_sizes")
def test_run_simulation(mock_vis_sizes, mock_vis_speed):
    """Test that the full simulation can run without errors."""
    # Run a small simulation
    result = run_simulation(iterations=1, num_vehicles_per_iteration=2)
    
    # Check that visualization functions were called
    mock_vis_speed.assert_called_once()
    mock_vis_sizes.assert_called_once()
    
    # Check that we got results
    assert len(result) == 2
    assert isinstance(result[0], dict)
    assert "signature" in result[0]
    assert "speed" in result[0]
    assert "size" in result[0]

if __name__ == "__main__":
    pytest.main(["-v", "test_utils.py"])
