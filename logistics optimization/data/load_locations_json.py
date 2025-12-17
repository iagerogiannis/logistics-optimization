# data/load_locations_json.py
# -*- coding: utf-8 -*-
"""
Module for loading location data from JSON files.
This allows users to provide custom locations for logistics centers,
sales outlets, and customers instead of generating them randomly.

Expected JSON format:
{
  "metadata": {
    "timestamp": "...",
    "num_logistics_centers": int,
    "num_sales_outlets": int,
    "num_customers": int
  },
  "locations": {
    "logistics_centers": [[lat, lon], [lat, lon], ...],
    "sales_outlets": [[lat, lon], [lat, lon], ...],
    "customers": [[lat, lon], [lat, lon], ...]
  }
}
"""

import json
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def load_locations_from_json(filepath: str) -> Dict[str, List]:
    """
    Loads location data from a JSON file.
    
    Args:
        filepath: Path to the JSON file containing location data
        
    Returns:
        Dictionary with keys 'logistics_centers', 'sales_outlets', 'customers'
        Each value is a list of [latitude, longitude] pairs
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the JSON structure is invalid
        json.JSONDecodeError: If the file is not valid JSON
    """
    logger.info(f"Loading locations from JSON file: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"Location file not found: {filepath}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {filepath}: {e}")
        raise json.JSONDecodeError(f"Invalid JSON format in file: {e.msg}", e.doc, e.pos)
    except Exception as e:
        logger.error(f"Unexpected error reading file {filepath}: {e}")
        raise
    
    # Validate structure
    if not isinstance(data, dict):
        raise ValueError("JSON root must be a dictionary")
    
    if 'locations' not in data:
        raise ValueError("JSON must contain 'locations' key")
    
    locations = data['locations']
    if not isinstance(locations, dict):
        raise ValueError("'locations' must be a dictionary")
    
    # Extract location arrays
    required_keys = ['logistics_centers', 'sales_outlets', 'customers']
    result = {}
    
    for key in required_keys:
        if key not in locations:
            logger.warning(f"Missing '{key}' in locations, using empty list")
            result[key] = []
        else:
            location_list = locations[key]
            if not isinstance(location_list, list):
                raise ValueError(f"'{key}' must be a list")
            
            # Validate each location is [lat, lon]
            validated_locations = []
            for i, loc in enumerate(location_list):
                if not isinstance(loc, (list, tuple)) or len(loc) != 2:
                    raise ValueError(f"Location {i} in '{key}' must be [latitude, longitude]")
                
                try:
                    lat = float(loc[0])
                    lon = float(loc[1])
                    
                    # Validate coordinate ranges
                    if not (-90 <= lat <= 90):
                        raise ValueError(f"Invalid latitude {lat} in '{key}' location {i} (must be -90 to 90)")
                    if not (-180 <= lon <= 180):
                        raise ValueError(f"Invalid longitude {lon} in '{key}' location {i} (must be -180 to 180)")
                    
                    validated_locations.append([lat, lon])
                except (ValueError, TypeError) as e:
                    raise ValueError(f"Invalid coordinate values in '{key}' location {i}: {e}")
            
            result[key] = validated_locations
    
    # Log summary
    logger.info(f"Loaded {len(result['logistics_centers'])} logistics centers, "
                f"{len(result['sales_outlets'])} sales outlets, "
                f"{len(result['customers'])} customers")
    
    # Validate minimum requirements
    if len(result['logistics_centers']) == 0:
        raise ValueError("At least one logistics center is required")
    
    return result


def validate_locations_structure(locations: Dict[str, List]) -> bool:
    """
    Validates that a locations dictionary has the correct structure.
    
    Args:
        locations: Dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(locations, dict):
        return False
    
    required_keys = ['logistics_centers', 'sales_outlets', 'customers']
    for key in required_keys:
        if key not in locations:
            return False
        if not isinstance(locations[key], list):
            return False
    
    return True


def get_location_counts(locations: Dict[str, List]) -> Dict[str, int]:
    """
    Returns the count of each location type.
    
    Args:
        locations: Dictionary containing location data
        
    Returns:
        Dictionary with counts for each location type
    """
    return {
        'num_logistics_centers': len(locations.get('logistics_centers', [])),
        'num_sales_outlets': len(locations.get('sales_outlets', [])),
        'num_customers': len(locations.get('customers', []))
    }