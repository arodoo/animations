# File: app/atmospheres/space_atmosphere.py
# Procedural space atmosphere generator with gravity-clustered starfields.
# Creates realistic star distributions using clustering algorithms.
# All Rights Reserved Arodi Emmanuel

import random
import math
from typing import Any, Dict, List, Tuple


def _generate_cluster_centers(num_clusters: int, radius: float) -> List[Tuple[float, float, float]]:
    """Generate random cluster centers in 3D space."""
    centers = []
    for _ in range(num_clusters):
        # Random spherical coordinates
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = random.uniform(radius * 0.3, radius)
        
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)
        centers.append((x, y, z))
    return centers


def _generate_stars_around_cluster(
    center: Tuple[float, float, float],
    count: int,
    spread: float,
    min_size: float,
    max_size: float
) -> List[Dict[str, Any]]:
    """Generate stars around a cluster center."""
    stars = []
    cx, cy, cz = center
    
    for _ in range(count):
        # Random offset from center
        offset_x = random.gauss(0, spread)
        offset_y = random.gauss(0, spread)
        offset_z = random.gauss(0, spread)
        
        x = cx + offset_x
        y = cy + offset_y
        z = cz + offset_z
        
        # Random size within bounds
        size = random.uniform(min_size, max_size)
        
        stars.append({
            'cmd': 'spawn_primitive',
            'args': {
                'type': 'plane',
                'name': f'Star_{random.randint(100000, 999999)}',
                'location': (x, y, z)
            }
        })
        
        # Scale command for size
        stars.append({
            'cmd': 'scale_object',
            'args': {
                'name': stars[-1]['args']['name'],
                'scale': (size, size, size)
            }
        })
    
    return stars


def generate_starfield(
    star_count: int = 1150,
    min_size: float = 0.01,
    max_size: float = 0.05,
    radius: float = 50.0,
    num_clusters: int = 8
) -> List[Dict[str, Any]]:
    """
    Generate a gravity-clustered starfield.
    
    Args:
        star_count: Total number of stars (1000-1300 recommended)
        min_size: Minimum star size
        max_size: Maximum star size
        radius: Sphere radius for distribution
        num_clusters: Number of gravity-like cluster regions
    
    Returns:
        List of command dictionaries for batch dispatch
    """
    commands = []
    
    # Generate cluster centers
    centers = _generate_cluster_centers(num_clusters, radius)
    
    # Distribute stars across clusters
    stars_per_cluster = star_count // num_clusters
    remaining_stars = star_count % num_clusters
    
    for i, center in enumerate(centers):
        count = stars_per_cluster
        if i < remaining_stars:
            count += 1
        
        # Spread varies per cluster for visual variety
        spread = random.uniform(radius * 0.1, radius * 0.3)
        
        cluster_stars = _generate_stars_around_cluster(
            center, count, spread, min_size, max_size
        )
        commands.extend(cluster_stars)
    
    return commands
