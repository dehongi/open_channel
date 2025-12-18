"""
Example 1: Channel Design

This example demonstrates how to use the open_channel library to design
a trapezoidal channel.

Problem:
Design an implementation of a trapezoidal channel to carry a discharge 
of 25 m³/s. The channel is to be excavated in earth with a Manning's n 
of 0.022. The available slope is 0.0005. The side slopes should be 2:1 (H:V).
The maximum allowable water depth is 2.5 meters to prevent overflow.

We need to find the minimum bottom width 'b' that satisfies these conditions.
"""

from open_channel import TrapezoidalChannel, solve_normal_depth, solve_discharge

def main():
    # Design constraints
    Q_design = 25.0  # m³/s
    n = 0.022
    s0 = 0.0005
    z = 2.0  # Side slope 2H:1V
    y_max = 2.5  # Maximum allowable depth in m

    print("--- Channel Design Problem ---")
    print(f"Design Discharge: {Q_design} m³/s")
    print(f"Slope: {s0}")
    print(f"Manning's n: {n}")
    print(f"Side slope z: {z}")
    print(f"Max allowable depth: {y_max} m")
    print("-" * 30)

    # Iteratively check different bottom widths
    # Start with b = 1.0m and increment by 0.5m
    b = 1.0
    found_solution = False
    
    print("\nIterating to find minimum bottom width...")
    print(f"{'Width (m)':<10} {'Normal Depth (m)':<20} {'Status':<10}")
    
    while b <= 20.0:  # Safety break at 20m
        # Create channel with current width
        channel = TrapezoidalChannel(b=b, z=z)
        
        # Calculate normal depth
        y_n = solve_normal_depth(channel, Q=Q_design, n=n, s=s0)
        
        status = "OK" if y_n <= y_max else "Too Deep"
        print(f"{b:<10.1f} {y_n:<20.3f} {status:<10}")
        
        if y_n <= y_max:
            print("-" * 30)
            print(f"\nSolution Found!")
            print(f"Minimum required bottom width: {b} m")
            print(f"Resulting Normal Depth: {y_n:.3f} m")
            
            # Verify capacity
            Q_actual = solve_discharge(channel, y=y_n, n=n, s=s0)
            print(f"Verified Discharge capacity: {Q_actual:.3f} m³/s")
            
            # Calculate other properties at design flow
            v = Q_actual / channel.area(y_n)
            fr = v / (9.81 * channel.hydraulic_depth(y_n))**0.5
            print(f"Flow Velocity: {v:.2f} m/s")
            print(f"Froude Number: {fr:.3f}")
            
            found_solution = True
            break
            
        b += 0.5
        
    if not found_solution:
        print("\nNo solution found within reasonable width limits.")

if __name__ == "__main__":
    main()
