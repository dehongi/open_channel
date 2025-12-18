"""
Example 4: Storm Drain Capacity (English Units)

This example demonstrates how to use the library for a storm drain calculation
using English units (ft, s, cfs).

Problem:
A 48-inch (4.0 ft) diameter concrete culvert (n=0.013) is laid on a 
slope of 0.005 ft/ft.
1. What is the full-pipe discharge capacity?
2. If the actual flow is 30 cubic feet per second (cfs), what is the normal depth?
3. Calculate the discharge if the pipe is half-full.
"""

from open_channel import CircularChannel, UnitSystem, solve_discharge, solve_normal_depth

def main():
    # Design Data
    diameter = 4.0  # feet (48 inches)
    n = 0.013
    s0 = 0.005
    unit_system = UnitSystem.ENGLISH
    
    print("--- Storm Drain Capacity (English Units) ---")
    print(f"Diameter: {diameter} ft")
    print(f"Manning's n: {n}")
    print(f"Slope: {s0}")
    print("-" * 40)

    channel = CircularChannel(D=diameter)

    # 1. Full-pipe discharge capacity
    # For Manning's equation in a pipe, "full" is often calculated at y = 0.938D 
    # for maximum discharge, but we'll use y = D for "full flow".
    Q_full = solve_discharge(
        channel=channel, 
        y=diameter - 0.001,  # Nearly full
        n=n, 
        s=s0, 
        unit_system=unit_system
    )
    print(f"Full-pipe capacity: {Q_full:.2f} cfs")

    # 2. Find normal depth for Q = 30 cfs
    Q_target = 30.0
    y_n = solve_normal_depth(
        channel=channel, 
        Q=Q_target, 
        n=n, 
        s=s0, 
        unit_system=unit_system,
        y_max=diameter * 0.9  # Avoid non-monotonic region for stable solution
    )
    print(f"\nFor Discharge = {Q_target} cfs:")
    print(f"Normal depth: {y_n:.3f} ft")
    print(f"Depth/Diameter ratio: {y_n/diameter:.3f}")

    # 3. Half-full discharge
    y_half = diameter / 2
    Q_half = solve_discharge(
        channel=channel, 
        y=y_half, 
        n=n, 
        s=s0, 
        unit_system=unit_system
    )
    print(f"\nHalf-full (y = {y_half} ft):")
    print(f"Discharge: {Q_half:.2f} cfs")
    
    # Check if Q_half is exactly half of Q_full? 
    # (Hydraulic radius is different, so no)
    ratio = (Q_half / Q_full) * 100
    print(f"Half-full discharge is {ratio:.1f}% of full capacity.")

if __name__ == "__main__":
    main()
