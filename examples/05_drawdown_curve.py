"""
Example 5: Drawdown Curve Visualization (M2 Profile)

This example calculates the water surface profile as flow approaches a 
free overfall at the end of a mild-sloped channel.

It demonstrates how to use the library to generate data for visualization
and saves the resulting plot as 'drawdown_profile.png'.
"""

import numpy as np
import matplotlib.pyplot as plt
from open_channel import RectangularChannel, solve_normal_depth, solve_critical_depth, standard_step_method

def main():
    # 1. Setup Channel Parameters
    Q = 10.0      # m³/s
    b = 3.0       # m
    n = 0.015
    s0 = 0.001
    
    channel = RectangularChannel(b=b)
    
    # 2. Calculate Reference Depths
    yn = solve_normal_depth(channel, Q, n, s0)
    yc = solve_critical_depth(channel, Q)
    
    print(f"Normal Depth (yn): {yn:.3f} m")
    print(f"Critical Depth (yc): {yc:.3f} m")
    
    # Verify M2 conditions: yn > y > yc
    if yn <= yc:
        print("Error: Slope is not MILD. Cannot form M2 profile.")
        return

    # 3. Calculate Profile
    # At a free overfall, the depth is approximately yc.
    # We will compute the profile starting from yc at x=0 and moving upstream.
    
    x_coords = []
    y_coords = []
    
    current_x = 0
    # Start slightly above yc to avoid numerical issues at the singularity Fr=1
    current_y = yc * 1.01 
    
    x_coords.append(current_x)
    y_coords.append(current_y)
    
    # Step upstream
    dx = -10.0 # 10m steps
    num_steps = 100
    
    print("\nCalculating profile upstream...")
    for _ in range(num_steps):
        try:
            next_x = current_x + dx
            next_y = standard_step_method(
                channel,
                x_start=current_x,
                y_start=current_y,
                x_target=next_x,
                Q=Q, n=n, s0=s0,
                y_min=yc, y_max=yn*1.1
            )
            
            x_coords.append(next_x)
            y_coords.append(next_y)
            
            current_x = next_x
            current_y = next_y
            
            # Stop if we are very close to normal depth
            if (yn - current_y) / yn < 0.005:
                break
                
        except ValueError:
            break

    # 4. Visualization
    plt.figure(figsize=(10, 6))
    
    # Convert to arrays for plotting
    x = np.array(x_coords)
    y_water = np.array(y_coords)
    
    # Calculate bed elevation (assume z=0 at overfall x=0)
    # z = z_start - S0 * x
    # Since we move upstream (negative x), bed rises.
    z_bed = -s0 * x
    
    # Plot Bed
    plt.plot(x, z_bed, 'k-', linewidth=2, label='Channel Bed')
    
    # Plot Water Surface (Bed + Depth)
    plt.plot(x, z_bed + y_water, 'b-', linewidth=2, label='Water Surface (M2)')
    
    # Plot Reference Lines
    plt.plot(x, z_bed + yn, 'g--', alpha=0.5, label='Normal Depth ($y_n$)')
    plt.plot(x, z_bed + yc, 'r--', alpha=0.5, label='Critical Depth ($y_c$)')
    
    # Styling
    plt.title(f'Drawdown Curve (M2 Profile) approaching Free Overfall\n$Q={Q} m^3/s, b={b}m, S_0={s0}$')
    plt.xlabel('Distance (m) - [0 is at Overfall]')
    plt.ylabel('Elevation (m)')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    
    # Save the plot
    output_file = 'drawdown_profile.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved to {output_file}")

if __name__ == "__main__":
    main()
