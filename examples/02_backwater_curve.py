"""
Example 2: Backwater Curve Analysis (M1 Profile)

This example calculates the water surface profile in a river channel 
upstream of a dam (M1 profile).

Problem:
A rectangular river channel 50m wide carries a discharge of 200 m³/s.
The bed slope is 0.0004 and Manning's n is 0.030.
A dam creates a water depth of 8.0 meters at the dam face (station 0).

We want to calculate the water surface profile upstream to find where
the depth returns to normal depth (within 1%).
"""


from open_channel import (
    RectangularChannel,
    solve_normal_depth,
    solve_critical_depth,
    standard_step_method
)

def main():
    # Channel Parameters
    width = 50.0 # m
    Q = 200.0    # m³/s
    n = 0.030
    s0 = 0.0004
    
    channel = RectangularChannel(b=width)
    
    print("--- Backwater Curve Calculation ---")
    
    # 1. Calculate Normal and Critical Depths
    y_n = solve_normal_depth(channel, Q, n, s0)
    y_c = solve_critical_depth(channel, Q)
    
    print(f"Normal Depth (yn): {y_n:.3f} m")
    print(f"Critical Depth (yc): {y_c:.3f} m")
    
    if y_n > y_c:
        print("Slope is MILD (yn > yc)")
    else:
        print("Slope is STEEP (yn < yc)")
        
    # 2. Setup Profile Calculation
    y_dam = 8.0  # Depth at dam
    print(f"\nDepth at dam: {y_dam} m")
    
    # Verify M1 profile conditions: y > yn > yc
    if y_dam > y_n > y_c:
        print("Conditions satisfy M1 profile (Backwater curve)")
    
    # Calculate profile upstream (negative x direction)
    stations = []
    depths = []
    
    current_x = 0
    current_y = y_dam
    step_size = -500 # m (upstream steps)
    
    stations.append(current_x)
    depths.append(current_y)
    
    print(f"\n{'Station (m)':<15} {'Depth (m)':<15}")
    print(f"{current_x:<15} {current_y:<15.3f}")
    
    # Loop until depth is close to normal depth (within 1%)
    while (current_y - y_n) / y_n > 0.01:
        next_x = current_x + step_size
        
        try:
            # Calculate depth at next station
            next_y = standard_step_method(
                channel,
                x_start=current_x,
                y_start=current_y,
                x_target=next_x,
                Q=Q,
                n=n,
                s0=s0
            )
            
            stations.append(next_x)
            depths.append(next_y)
            
            # Print every 2km (4 steps)
            if abs(next_x) % 2000 == 0:
                print(f"{next_x:<15} {next_y:<15.3f}")
                
            current_x = next_x
            current_y = next_y
            
        except ValueError as e:
            print(f"Calculation stopped: {e}")
            break
            
    print(f"{current_x:<15} {current_y:<15.3f}")
    print(f"\nNormal depth reached approx. {abs(current_x)/1000:.2f} km upstream.")

if __name__ == "__main__":
    main()
