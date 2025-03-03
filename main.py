import logging
import os
import time
from pathlib import Path
from utils import (
    generate_vehicle_data, 
    simulate_sensor_data_processing, 
    simulate_data_analysis, 
    visualize_speed_distribution,
    visualize_vehicle_sizes,
    run_simulation
)

def setup_logging():
    """
    Set up logging configuration with file and console handlers.
    
    Creates a logs directory if it doesn't exist and configures logging
    to write to both a timestamped log file and the console.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging to file and console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f"traffic_system_{int(time.time())}.log"),
            logging.StreamHandler()
        ]
    )

def main():
    """
    Main function to run the traffic system simulation.
    
    Executes both a single run simulation and a multi-iteration simulation,
    with visualization of the results.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Single run simulation
        logger.info("Starting traffic system simulation...")
        
        num_vehicles = 50  # Increased for better visualization
        logger.info(f"Generating data for {num_vehicles} vehicles...")
        vehicle_data = generate_vehicle_data(num_vehicles)
        
        logger.info("Processing sensor data...")
        processed_data = simulate_sensor_data_processing(vehicle_data)
        
        logger.info("Analyzing processed data...")
        analyzed_data = simulate_data_analysis(processed_data)
        
        logger.info("Visualizing results...")
        visualize_speed_distribution(analyzed_data)
        visualize_vehicle_sizes(analyzed_data)
        
        # Multi-iteration simulation
        logger.info("\nStarting multi-iteration simulation...")
        run_simulation(iterations=3, num_vehicles_per_iteration=20)
        
        logger.info("Simulation completed successfully.")
        logger.info(f"Results saved to {output_dir.absolute()}")
        
    except Exception as e:
        logger.error(f"An error occurred during the simulation: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
