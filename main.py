
import logging
from utils import generate_vehicle_data, simulate_sensor_data_processing, simulate_data_analysis, visualize_speed_distribution

def main():
    logging.basicConfig(level=logging.INFO)
    
    try:
        num_vehicles = 10
        logging.info(f"Generating data for {num_vehicles} vehicles...")
        vehicle_data = generate_vehicle_data(num_vehicles)
        
        logging.info("Processing sensor data...")
        processed_data = simulate_sensor_data_processing(vehicle_data)
        
        logging.info("Analyzing processed data...")
        analyzed_data = simulate_data_analysis(processed_data)
        
        logging.info("Visualizing speed distribution...")
        visualize_speed_distribution(analyzed_data)
        
        logging.info("Simulation completed successfully.")
        
    except Exception as e:
        logging.error(f"An error occurred during the simulation: {e}")
        raise

if __name__ == "__main__":
    main()




