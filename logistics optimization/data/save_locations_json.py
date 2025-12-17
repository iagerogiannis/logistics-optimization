import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def save_locations_json(generated_locations, output_dir='output/generated_data'):
    """
    Save generated locations to a JSON file.
    
    Args:
        generated_locations (dict): Dictionary with 'logistics_centers', 'sales_outlets', 'customers'
        output_dir (str): Directory to save the file
        
    Returns:
        str: Path to saved file, or None if failed
    """
    if not generated_locations:
        logger.warning("No locations to save.")
        return None
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'locations_{timestamp}.json'
    filepath = os.path.join(output_dir, filename)
    
    try:
        # Prepare data for JSON (add metadata)
        data_to_save = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'num_logistics_centers': len(generated_locations.get('logistics_centers', [])),
                'num_sales_outlets': len(generated_locations.get('sales_outlets', [])),
                'num_customers': len(generated_locations.get('customers', []))
            },
            'locations': generated_locations
        }
        
        # Write to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2)
        
        logger.info(f"✓ Locations saved to: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"✗ Error saving locations to JSON: {e}")
        return None


# Example usage - add this right after your generate_locations call:
"""
generated_locations = generate_locations(...)

# Save to JSON
save_generated_locations_json(generated_locations)
"""