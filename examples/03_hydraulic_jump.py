"""
Example 3: Hydraulic Jump Analysis

This example demonstrates the analysis of a hydraulic jump in a rectangular 
stilling basin.

Problem:
A spillway discharges 50 m³/s into a rectangular stilling basin that is 
6.0 meters wide. The flow enters the basin with a velocity of 12 m/s.
We need to determine:
1. The Froude number of the incoming flow.
2. The conjugate depth (sequent depth) needed to stabilize the jump.
3. The energy loss dissipated by the jump.
4. The efficiency of the jump.
"""

from open_channel import RectangularChannel, solve_conjugate_depth, calculate_froude

def main():
    # Given Data
    Q = 50.0      # m³/s
    width = 6.0   # m
    v1 = 12.0     # m/s
    
    channel = RectangularChannel(b=width)
    
    print("--- Hydraulic Jump Analysis ---")
    print(f"Discharge: {Q} m³/s")
    print(f"Channel Width: {width} m")
    print(f"Inflow Velocity: {v1} m/s")
    
    # 1. Calculate Upstream Depth (y1)
    # Q = v * A = v * (b * y) => y = Q / (v * b)
    y1 = Q / (v1 * width)
    print(f"\nUpstream Depth (y1): {y1:.3f} m")
    
    # 2. Calculate Froude Number (Fr1)
    Fr1 = calculate_froude(channel, y=y1, Q=Q)
    print(f"Upstream Froude Number (Fr1): {Fr1:.3f}")
    
    if Fr1 <= 1.0:
        print("Flow is subcritical or critical. Hydraulic jump cannot occur.")
        return
        
    print("Flow is Supercritical (Fr > 1). Jump is possible.")
    
    # Categorize Jump Type (based on USBR)
    if 1.0 < Fr1 <= 1.7:
        jump_type = "Undular Jump"
    elif 1.7 < Fr1 <= 2.5:
        jump_type = "Weak Jump"
    elif 2.5 < Fr1 <= 4.5:
        jump_type = "Oscillating Jump"
    elif 4.5 < Fr1 <= 9.0:
        jump_type = "Steady Jump"
    else:
        jump_type = "Strong Jump"
        
    print(f"Jump Classification: {jump_type}")
    
    # 3. Calculate Conjugate Depth (y2) and Energy Dissipation
    y2, delta_E = solve_conjugate_depth(channel, y1=y1, Fr1=Fr1)
    
    print(f"\nConjugate (Sequent) Depth (y2): {y2:.3f} m")
    print(f"Energy Loss (ΔE): {delta_E:.3f} m")
    
    # 4. Calculate Efficiency
    # Efficiency = E2 / E1
    # Specific Energy E = y + v^2/2g
    g = 9.81
    E1 = y1 + (v1**2) / (2*g)
    v2 = Q / (width * y2)
    E2 = y2 + (v2**2) / (2*g)
    
    efficiency = (E2 / E1) * 100
    percent_dissipation = (delta_E / E1) * 100
    
    print(f"\nSpecific Energy E1: {E1:.3f} m")
    print(f"Specific Energy E2: {E2:.3f} m")
    print(f"Jump Efficiency: {efficiency:.1f}%")
    print(f"Energy Dissipated: {percent_dissipation:.1f}%")
    
    # Height of the jump
    height = y2 - y1
    print(f"Height of Jump: {height:.3f} m")

if __name__ == "__main__":
    main()
