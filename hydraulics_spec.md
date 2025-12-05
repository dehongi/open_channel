# Functional Specification: Python Open Channel Hydraulics Library

## 1. Project Overview
**Goal:** Develop a modular Python library for solving open channel hydraulics problems. The library must handle geometric calculations, uniform flow, critical flow, gradually varied flow profiles, and hydraulic structures.

**Tech Stack:**
* Language: Python 3.x
* Dependencies: `numpy` (vectorization), `scipy.optimize` (root finding/numerical solvers).

---

## 2. Module 1: Channel Geometry Architecture
**Requirement:** The library must use an Object-Oriented approach. Define a base class `Channel` and subclasses for specific shapes.

### 2.1 Geometric Parameters
All channel classes must store:
* `b`: Bottom width (m or ft)
* `z`: Side slope (z horizontal : 1 vertical) - *Input 0 for rectangular*
* `D`: Diameter (for circular sections)

### 2.2 Required Methods
Every shape class must implement these methods taking Water Depth (`y`) as an input:

1.  **Area ($A$):** Cross-sectional flow area.
2.  **Wetted Perimeter ($P$):** Length of wetted surface.
3.  **Hydraulic Radius ($R$):** $R = A / P$
4.  **Top Width ($T$):** Width at the free surface.
5.  **Hydraulic Depth ($D_h$):** $D_h = A / T$

### 2.3 Geometric Formulas

| Shape | Area ($A$) | Wetted Perimeter ($P$) | Top Width ($T$) |
| :--- | :--- | :--- | :--- |
| **Rectangular** | $b \cdot y$ | $b + 2y$ | $b$ |
| **Trapezoidal** | $(b + zy)y$ | $b + 2y\sqrt{1+z^2}$ | $b + 2zy$ |
| **Triangular** | $zy^2$ | $2y\sqrt{1+z^2}$ | $2zy$ |
| **Circular** | $\frac{D^2}{8}(\theta - \sin\theta)$ | $\frac{1}{2}\theta D$ | $D \sin(\theta/2)$ |

*Note for Circular:* $\theta = 2\arccos(1 - \frac{2y}{D})$

---

## 3. Module 2: Uniform Flow (Manning's Equation)
**Physics:** Assumes Energy Slope ($S_f$) matches Bed Slope ($S_0$).

**Equation:**
$$Q = \frac{k}{n} A R^{2/3} S_0^{1/2}$$
* $k = 1.0$ (SI) or $1.486$ (Imperial)

### 3.1 Functions to Implement
1.  `solve_discharge(channel, y, n, s)`: Calculate $Q$ directly.
2.  `solve_normal_depth(channel, Q, n, s)`: Calculate $y_n$.
    * **Constraint:** This is implicit. Use a numerical solver (e.g., Newton-Raphson) to find $y$ where $Q_{calc}(y) - Q_{target} = 0$.

---

## 4. Module 3: Critical Flow & Energy
**Physics:** Analyzes flow regimes (Subcritical vs. Supercritical).

### 4.1 Froude Number
**Equation:**
$$Fr = \frac{V}{\sqrt{g D_h}}$$

### 4.2 Functions to Implement
1.  `calculate_froude(channel, y, Q)`: Returns $Fr$.
2.  `solve_critical_depth(channel, Q)`: Calculate $y_c$.
    * **Logic:** Find depth where $Fr = 1$ (or Specific Energy is minimum).
    * **Solver:** Use `scipy.optimize` to solve $1 - \frac{Q^2 T}{g A^3} = 0$.
3.  `solve_alternate_depths(channel, E, Q)`: Given Specific Energy ($E$), find the two possible depths (subcritical and supercritical) excluding the critical depth.

---

## 5. Module 4: Gradually Varied Flow (GVF)
**Physics:** Calculates water surface profiles (e.g., M1, M2, S1 curves).

**Differential Equation:**
$$\frac{dy}{dx} = \frac{S_0 - S_f}{1 - Fr^2}$$
* Where $S_f = \frac{n^2 Q^2}{A^2 R^{4/3}}$ (SI Units)

### 5.1 Methods to Implement
1.  **Direct Step Method:**
    * *Input:* Defined upstream depth, defined downstream depth, geometry, $Q$.
    * *Output:* Distance ($\Delta x$) between the two depths.
    * *Use Case:* Prismatic (artificial) channels.

2.  **Standard Step Method:**
    * *Input:* Starting Station (x, y), Target Station (x), geometry, $Q$.
    * *Output:* Depth ($y$) at Target Station.
    * *Logic:* Iterative solution required to balance energy equation between two stations.

---

## 6. Module 5: Hydraulic Structures

### 6.1 Hydraulic Jump
**Function:** `solve_conjugate_depth(channel, y1, Fr1)`
* Calculate the downstream subcritical depth ($y_2$) given upstream supercritical conditions.
* Calculate Energy Loss ($\Delta E$).

### 6.2 Weirs
Implement standard discharge coefficients:
1.  **Rectangular Weir:** $Q = C_d L H^{3/2}$
2.  **V-Notch Weir:** $Q = C_d \tan(\frac{\theta}{2}) H^{5/2}$

---

## 7. Implementation Constraints & Guidelines

1.  **Unit Management:** The library must allow initialization with a unit system ('SI' or 'English').
    * SI: $g=9.81$, $k=1.0$
    * English: $g=32.2$, $k=1.486$
2.  **Robust Solvers:** Do not write custom loop-based solvers. Use `scipy.optimize.brentq` or `newton`.
3.  **Validation:** Ensure inputs are physical (e.g., $y > 0$, $n > 0$, $b > 0$). Raise `ValueError` for invalid inputs.
4.  **Documentation:** All functions must have docstrings describing inputs, outputs, and units.