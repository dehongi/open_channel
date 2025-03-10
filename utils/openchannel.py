import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, root_scalar

class OpenChannel:
    """Base class for open channel calculations"""
    
    def __init__(self, Q=None, g=9.81, n=None, S0=None):
        """
        Initialize with discharge, gravitational acceleration, Manning's n, and channel slope
        
        Parameters:
        Q (float): Discharge in m³/s (optional for some calculations)
        g (float): Gravitational acceleration in m/s², default is 9.81
        n (float): Manning's roughness coefficient (optional for some calculations)
        S0 (float): Channel slope (optional for some calculations)
        """
        self.Q = Q
        self.g = g
        self.n = n
        self.S0 = S0
    
    def area(self, y):
        """Flow area as a function of depth"""
        raise NotImplementedError("Subclass must implement abstract method")
    
    def width(self, y):
        """Top width as a function of depth"""
        raise NotImplementedError("Subclass must implement abstract method")
    
    def wetted_perimeter(self, y):
        """Wetted perimeter as a function of depth"""
        raise NotImplementedError("Subclass must implement abstract method")
    
    def hydraulic_radius(self, y):
        """Hydraulic radius as a function of depth"""
        return self.area(y) / self.wetted_perimeter(y)
    
    def critical_depth_function(self, y):
        """
        Function to minimize to find critical depth
        At critical depth, Q²T/gA³ = 1, so we minimize (Q²T/gA³ - 1)²
        """
        if y <= 0:
            return float('inf')
        A = self.area(y)
        T = self.width(y)
        return (self.Q**2 * T / (self.g * A**3) - 1)**2
    
    def calculate_critical_depth(self, y_max=10):
        """
        Calculate critical depth using numerical optimization
        
        Parameters:
        y_max (float): Maximum depth to consider for optimization
        
        Returns:
        float: Critical depth
        """
        if self.Q is None:
            raise ValueError("Discharge (Q) must be set to calculate critical depth")
            
        result = minimize_scalar(
            self.critical_depth_function,
            bounds=(0.001, y_max),
            method='bounded'
        )
        return result.x
    
    def normal_depth_function(self, y):
        """
        Function to find root of to calculate normal depth
        Uses Manning's equation: Q = (1/n) * A * R^(2/3) * S0^(1/2)
        """
        if y <= 0:
            return float('inf')
        A = self.area(y)
        R = self.hydraulic_radius(y)
        Q_manning = (1/self.n) * A * R**(2/3) * np.sqrt(self.S0)
        return self.Q - Q_manning
    
    def calculate_normal_depth(self, y_min=0.001, y_max=10):
        """
        Calculate normal depth using Manning's equation
        
        Parameters:
        y_min (float): Minimum depth to consider
        y_max (float): Maximum depth to consider
        
        Returns:
        float: Normal depth
        """
        if self.Q is None or self.n is None or self.S0 is None:
            raise ValueError("Discharge (Q), Manning's n, and channel slope (S0) must be set to calculate normal depth")
            
        try:
            result = root_scalar(
                self.normal_depth_function,
                bracket=[y_min, y_max],
                method='brentq'
            )
            return result.root
        except ValueError:
            # If bracketing fails, try optimization approach
            def abs_func(y):
                return abs(self.normal_depth_function(y))
                
            result = minimize_scalar(
                abs_func,
                bounds=(y_min, y_max),
                method='bounded'
            )
            return result.x
    
    def calculate_discharge(self, y):
        """
        Calculate discharge using Manning's equation for a given depth
        
        Parameters:
        y (float): Depth of flow
        
        Returns:
        float: Discharge in m³/s
        """
        if self.n is None or self.S0 is None:
            raise ValueError("Manning's n and channel slope (S0) must be set to calculate discharge")
            
        A = self.area(y)
        R = self.hydraulic_radius(y)
        Q = (1/self.n) * A * R**(2/3) * np.sqrt(self.S0)
        return Q
    
    def set_parameters(self, Q=None, n=None, S0=None):
        """Update parameters for the channel"""
        if Q is not None:
            self.Q = Q
        if n is not None:
            self.n = n
        if S0 is not None:
            self.S0 = S0
    
    def plot_energy_curve(self, y_range=None):
        """
        Plot the specific energy curve
        
        Parameters:
        y_range (tuple): Range of depths to plot (min, max)
        """
        if self.Q is None:
            raise ValueError("Discharge (Q) must be set to plot energy curve")
            
        if y_range is None:
            yc = self.calculate_critical_depth()
            y_range = (0.1*yc, 3*yc)
            
        depths = np.linspace(y_range[0], y_range[1], 100)
        energies = []
        
        for y in depths:
            A = self.area(y)
            V = self.Q / A
            E = y + V**2 / (2 * self.g)
            energies.append(E)
        
        plt.figure(figsize=(10, 6))
        plt.plot(energies, depths)
        plt.grid(True)
        plt.xlabel('Specific Energy (m)')
        plt.ylabel('Depth (m)')
        plt.title('Specific Energy Diagram')
        
        # Mark critical depth
        yc = self.calculate_critical_depth()
        Ac = self.area(yc)
        Vc = self.Q / Ac
        Ec = yc + Vc**2 / (2 * self.g)
        plt.plot(Ec, yc, 'ro', label=f'Critical Point (yc = {yc:.3f} m)')
        
        # Mark normal depth if parameters are available
        if self.n is not None and self.S0 is not None:
            try:
                yn = self.calculate_normal_depth()
                An = self.area(yn)
                Vn = self.Q / An
                En = yn + Vn**2 / (2 * self.g)
                plt.plot(En, yn, 'go', label=f'Normal Depth (yn = {yn:.3f} m)')
            except Exception as e:
                print(f"Could not plot normal depth: {e}")
        
        plt.legend()
        plt.show()
        
    def plot_rating_curve(self, y_max=None, points=100):
        """
        Plot the rating curve (discharge vs depth)
        
        Parameters:
        y_max (float): Maximum depth to plot
        points (int): Number of points to plot
        """
        if self.n is None or self.S0 is None:
            raise ValueError("Manning's n and channel slope (S0) must be set to plot rating curve")
            
        if y_max is None:
            if self.Q is not None:
                try:
                    yn = self.calculate_normal_depth()
                    y_max = 2 * yn
                except:
                    y_max = 5
            else:
                y_max = 5
                
        depths = np.linspace(0.01, y_max, points)
        discharges = [self.calculate_discharge(y) for y in depths]
        
        plt.figure(figsize=(10, 6))
        plt.plot(discharges, depths)
        plt.grid(True)
        plt.xlabel('Discharge (m³/s)')
        plt.ylabel('Depth (m)')
        plt.title('Rating Curve')
        
        # Mark current Q and normal depth if available
        if self.Q is not None:
            try:
                yn = self.calculate_normal_depth()
                plt.plot(self.Q, yn, 'go', label=f'Normal Depth (Q = {self.Q:.2f} m³/s, yn = {yn:.3f} m)')
            except Exception as e:
                print(f"Could not plot normal depth: {e}")
        
        plt.legend()
        plt.show()


class RectangularChannel(OpenChannel):
    """Rectangular channel cross-section"""
    
    def __init__(self, b, Q=None, g=9.81, n=None, S0=None):
        """
        Initialize rectangular channel
        
        Parameters:
        b (float): Channel width in m
        Q (float): Discharge in m³/s (optional)
        g (float): Gravitational acceleration in m/s²
        n (float): Manning's roughness coefficient (optional)
        S0 (float): Channel slope (optional)
        """
        super().__init__(Q, g, n, S0)
        self.b = b
    
    def area(self, y):
        """Flow area as a function of depth"""
        return self.b * y
    
    def width(self, y):
        """Top width is constant for rectangular channel"""
        return self.b
    
    def wetted_perimeter(self, y):
        """Wetted perimeter as a function of depth"""
        return self.b + 2 * y
    
    def calculate_critical_depth_analytical(self):
        """
        Calculate critical depth using analytical formula for rectangular channels
        yc = (q²/g)^(1/3) where q = Q/b
        
        Returns:
        float: Critical depth
        """
        if self.Q is None:
            raise ValueError("Discharge (Q) must be set to calculate critical depth")
            
        q = self.Q / self.b  # unit discharge
        return (q**2 / self.g)**(1/3)


class TrapezoidalChannel(OpenChannel):
    """Trapezoidal channel cross-section"""
    
    def __init__(self, b, z, Q=None, g=9.81, n=None, S0=None):
        """
        Initialize trapezoidal channel
        
        Parameters:
        b (float): Bottom width in m
        z (float): Side slope (horizontal:vertical)
        Q (float): Discharge in m³/s (optional)
        g (float): Gravitational acceleration in m/s²
        n (float): Manning's roughness coefficient (optional)
        S0 (float): Channel slope (optional)
        """
        super().__init__(Q, g, n, S0)
        self.b = b
        self.z = z
    
    def area(self, y):
        """Flow area as a function of depth"""
        return self.b * y + self.z * y**2
    
    def width(self, y):
        """Top width as a function of depth"""
        return self.b + 2 * self.z * y
    
    def wetted_perimeter(self, y):
        """Wetted perimeter as a function of depth"""
        sloping_sides = 2 * y * np.sqrt(1 + self.z**2)
        return self.b + sloping_sides


class TriangularChannel(OpenChannel):
    """Triangular channel cross-section"""
    
    def __init__(self, z, Q=None, g=9.81, n=None, S0=None):
        """
        Initialize triangular channel
        
        Parameters:
        z (float): Side slope (horizontal:vertical)
        Q (float): Discharge in m³/s (optional)
        g (float): Gravitational acceleration in m/s²
        n (float): Manning's roughness coefficient (optional)
        S0 (float): Channel slope (optional)
        """
        super().__init__(Q, g, n, S0)
        self.z = z
    
    def area(self, y):
        """Flow area as a function of depth"""
        return self.z * y**2
    
    def width(self, y):
        """Top width as a function of depth"""
        return 2 * self.z * y
    
    def wetted_perimeter(self, y):
        """Wetted perimeter as a function of depth"""
        return 2 * y * np.sqrt(1 + self.z**2)


class CircularChannel(OpenChannel):
    """Circular channel (pipe) cross-section"""
    
    def __init__(self, D, Q=None, g=9.81, n=None, S0=None):
        """
        Initialize circular channel
        
        Parameters:
        D (float): Diameter in m
        Q (float): Discharge in m³/s (optional)
        g (float): Gravitational acceleration in m/s²
        n (float): Manning's roughness coefficient (optional)
        S0 (float): Channel slope (optional)
        """
        super().__init__(Q, g, n, S0)
        self.D = D
        self.R = D / 2
    
    def theta(self, y):
        """Calculate the angle subtended by the water surface from the center"""
        if y >= self.D:
            return 2 * np.pi
        elif y <= 0:
            return 0
        else:
            return 2 * np.arccos(1 - 2 * y / self.D)
    
    def area(self, y):
        """Flow area as a function of depth"""
        if y >= self.D:
            return np.pi * self.R**2
        elif y <= 0:
            return 0
        else:
            theta = self.theta(y)
            return 0.5 * self.R**2 * (theta - np.sin(theta))
    
    def width(self, y):
        """Top width as a function of depth"""
        if y >= self.D:
            return 0  # Full pipe has no free surface
        elif y <= 0:
            return 0
        else:
            return 2 * self.R * np.sin(0.5 * self.theta(y))
    
    def wetted_perimeter(self, y):
        """Wetted perimeter as a function of depth"""
        if y >= self.D:
            return np.pi * self.D  # Full perimeter for a full pipe
        elif y <= 0:
            return 0
        else:
            theta = self.theta(y)
            return self.R * theta


class ParabolicChannel(OpenChannel):
    """Parabolic channel cross-section"""
    
    def __init__(self, c, Q=None, g=9.81, n=None, S0=None):
        """
        Initialize parabolic channel
        
        Parameters:
        c (float): Shape parameter such that width = 2*c*sqrt(y)
        Q (float): Discharge in m³/s (optional)
        g (float): Gravitational acceleration in m/s²
        n (float): Manning's roughness coefficient (optional)
        S0 (float): Channel slope (optional)
        """
        super().__init__(Q, g, n, S0)
        self.c = c
    
    def area(self, y):
        """Flow area as a function of depth"""
        return (2/3) * self.c * y**(3/2)
    
    def width(self, y):
        """Top width as a function of depth"""
        return 2 * self.c * np.sqrt(y)
    
    def wetted_perimeter(self, y):
        """
        Wetted perimeter as a function of depth
        For a parabola z = c²y, the arc length is calculated using an approximation
        """
        T = self.width(y)
        # Approximate the wetted perimeter using the top width plus an adjustment
        # for the curvature of the parabola
        return T + 0.2 * T  # Simplified approximation


# Example usage
def main():
    print("\n ===== Open Channel Flow Calculator =====\n")
    
    channel_type = input("""
Select channel type:
1. Rectangular
2. Trapezoidal
3. Triangular
4. Circular
5. Parabolic
Enter the number (1-5): """)
    
    # Get channel geometry parameters
    if channel_type == '1':
        b = float(input("Enter channel width (m): "))
        channel = RectangularChannel(b)
        
    elif channel_type == '2':
        b = float(input("Enter bottom width (m): "))
        z = float(input("Enter side slope (horizontal:vertical): "))
        channel = TrapezoidalChannel(b, z)
        
    elif channel_type == '3':
        z = float(input("Enter side slope (horizontal:vertical): "))
        channel = TriangularChannel(z)
        
    elif channel_type == '4':
        D = float(input("Enter pipe diameter (m): "))
        channel = CircularChannel(D)
        
    elif channel_type == '5':
        c = float(input("Enter shape parameter c: "))
        channel = ParabolicChannel(c)
        
    else:
        print("Invalid selection. Exiting.")
        return
    
    # Get hydraulic parameters
    print("\n --- Hydraulic Parameters ---")
    
    calc_mode = input("""
Select calculation mode:
1. Calculate normal depth from discharge
2. Calculate discharge from normal depth
3. Calculate both critical and normal depths
Enter the number (1-3): """)
    
    if calc_mode == '1' or calc_mode == '3':
        Q = float(input("Enter discharge (m³/s): "))
        n = float(input("Enter Manning's roughness coefficient: "))
        S0 = float(input("Enter channel slope (m/m): "))
        channel.set_parameters(Q=Q, n=n, S0=S0)
        
        print("\n --- Results ---")
        try:
            yn = channel.calculate_normal_depth()
            print(f"Normal depth: {yn:.4f} m")
        except Exception as e:
            print(f"Could not calculate normal depth: {e}")
            
        try:
            yc = channel.calculate_critical_depth()
            print(f"Critical depth: {yc:.4f} m")
            
            if channel_type == '1':
                analytical_yc = channel.calculate_critical_depth_analytical()
                print(f"Analytical critical depth: {analytical_yc:.4f} m")
                
            # Flow regime
            if yn > yc:
                print("Flow regime: Subcritical (Fr < 1)")
            elif yn < yc:
                print("Flow regime: Supercritical (Fr > 1)")
            else:
                print("Flow regime: Critical (Fr = 1)")
                
        except Exception as e:
            print(f"Could not calculate critical depth: {e}")
    
    elif calc_mode == '2':
        y = float(input("Enter normal depth (m): "))
        n = float(input("Enter Manning's roughness coefficient: "))
        S0 = float(input("Enter channel slope (m/m): "))
        channel.set_parameters(n=n, S0=S0)
        
        print("\n --- Results ---")
        try:
            Q = channel.calculate_discharge(y)
            print(f"Discharge: {Q:.4f} m³/s")
            channel.set_parameters(Q=Q)
            
            # Calculate and display velocity
            A = channel.area(y)
            V = Q / A
            print(f"Average velocity: {V:.4f} m/s")
            
            # Calculate Froude number
            T = channel.width(y)
            D = A / T  # Hydraulic depth
            Fr = V / np.sqrt(channel.g * D)
            print(f"Froude number: {Fr:.4f}")
            
            if Fr < 1:
                print("Flow regime: Subcritical (Fr < 1)")
            elif Fr > 1:
                print("Flow regime: Supercritical (Fr > 1)")
            else:
                print("Flow regime: Critical (Fr = 1)")
                
        except Exception as e:
            print(f"Could not calculate discharge: {e}")
    
    # Ask for plots
    print("\n --- Visualization Options ---")
    
    plot_choice = input("""
Select visualization:
1. Specific Energy Diagram
2. Rating Curve
3. Both
4. None
Enter the number (1-4): """)
    
    if plot_choice == '1' or plot_choice == '3':
        try:
            channel.plot_energy_curve()
        except Exception as e:
            print(f"Could not plot energy curve: {e}")
    
    if plot_choice == '2' or plot_choice == '3':
        try:
            channel.plot_rating_curve()
        except Exception as e:
            print(f"Could not plot rating curve: {e}")


if __name__ == "__main__":
    main()