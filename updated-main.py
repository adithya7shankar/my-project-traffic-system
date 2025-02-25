import logging
import os
import time
from utils import (
    generate_vehicle_data, 
    simulate_sensor_data_processing, 
    simulate_data_analysis, 
    visualize_speed_distribution,
    run_simulation
)

def setup_logging():
    """Set up logging configuration."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging to file and console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{log_dir}/traffic_system_{int(time.time())}.log"),
            logging.StreamHandler()
        ]
    )

def main():
    """Main function to run the traffic system simulation."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Single run simulation
        logger.info("Starting traffic system simulation...")
        
        num_vehicles = 50  # Increased for better visualization
        logger.info(f"Generating data for {num_vehicles} vehicles...")
        vehicle_data = generate_vehicle_data(num_vehicles)
        
        logger.info("Processing sensor data...")
        processed_data = simulate_sensor_data_processing(vehicle_data)
        
        logger.info("Analyzing processed data...")
        analyzed_data = simulate_data_analysis(processed_data)
        
        logger.info("Visualizing speed distribution...")
        visualize_speed_distribution(analyzed_data)
        
        # Multi-iteration simulation
        logger.info("\nStarting multi-iteration simulation...")
        run_simulation(iterations=3, num_vehicles_per_iteration=20)
        
        logger.info("Simulation completed successfully.")
        
    except Exception as e:
        logger.error(f"An error occurred during the simulation: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
