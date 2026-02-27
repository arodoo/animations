# File: scenes/resonance_box/animations/_strobe.py
# Pure mathematical extraction for calculating Music Box strobe keyframes.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_strobe_keyframes(
    mat_name: str, period: int, total_frames: int
) -> List[Dict]:
    """Calculate and return keyframe commands for rhythmic orbital flashes.
    
    The burst triggers precisely when the planet crosses the mathematical 'North'
    (positive Y-axis), evaluating to formula: frame = period * (0.25 + k)
    
    Args:
        mat_name: Target material name
        period: Planet orbital period
        total_frames: Max timeline frame count
    """
    cmds: List[Dict] = []
    
    # Baseline darkness at frame 1 to ensure zero-state initialization
    cmds.append({'cmd': 'keyframe_material_emission', 'args': {
        'material': mat_name, 'strength': 0.0, 'frame': 1
    }})
    
    # Rhythmic Strobe Logic (Music Box metronome pattern)
    max_k = int(total_frames / period) + 1
    for k in range(max_k):
        # Precise frame of crossing the Y+ Pole
        strobe_frame = int(period * (0.25 + k))
        
        if 1 <= strobe_frame <= total_frames:
            # 1. Plunge to absolute dark instantly prior to impact
            if strobe_frame - 2 > 0:
                cmds.append({'cmd': 'keyframe_material_emission', 'args': {
                    'material': mat_name, 'strength': 0.0, 'frame': strobe_frame - 2
                }})
            
            # 2. Massive burst of physical emission node on intersection
            cmds.append({'cmd': 'keyframe_material_emission', 'args': {
                'material': mat_name, 'strength': 100.0, 'frame': strobe_frame
            }})
            
            # 3. Sloped gradual thermal decay
            decay_frame = min(strobe_frame + 60, total_frames)
            cmds.append({'cmd': 'keyframe_material_emission', 'args': {
                'material': mat_name, 'strength': 0.0, 'frame': decay_frame
            }})
            
    return cmds
