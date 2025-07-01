# This script computes a geodesic on the surface z = a * exp(-x^2 - y^2)
# using a boundary value problem (BVP). The geodesic starts at (5, 5) and ends at (-5, -5),
# and the initial guess for the path is shaped like a semicircle in 3D.

from numpy import *
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

# Surface amplitude
a = 3

# Gaussian surface height function
def f(x, y):
    return a * exp(-x**2 - y**2)

# Gradient of F(x, y, z) = f(x, y) - z
def gradF(x, y, z):
    Fx = -2 * x * a * exp(-x**2 - y**2)
    Fy = -2 * y * a * exp(-x**2 - y**2)
    Fz = -1
    return stack((Fx, Fy, Fz))

# Hessian of F(x, y, z)
def HF(x, y, z):
    exp_term = exp(-x**2 - y**2)
    Fxx = 2 * a * (2 * x**2 - 1) * exp_term
    Fxy = 4 * a * x * y * exp_term
    Fyy = 2 * a * (2 * y**2 - 1) * exp_term
    return array([[Fxx, Fxy, 0], [Fxy, Fyy, 0], [0, 0, 0]])

# Start and end points on the surface
x1, y1, z1 = 5.0, 5.0, f(5, 5)
x2, y2, z2 = -5.0, -5.0, f(-5, -5)

# BVP boundary conditions
def bc(ya, yb):
    return array([
        ya[0] - x1, ya[1] - y1, ya[2] - z1,
        yb[0] - x2, yb[1] - y2, yb[2] - z2
    ])

# Initial guess: a semicircular arc in 3D from (x1, y1) to (x2, y2)
R = 3.0  # radius of semicircle
t_vals = linspace(0, 1, 100)
theta = linspace(0, pi, len(t_vals))

# Use a semicircle in the x-y plane with z = 0
y_guess = zeros((6, len(t_vals)))
y_guess[:3, :] = vstack((
    R * cos(theta),
    R * sin(theta),
    zeros_like(theta)
))

# Geodesic system of ODEs
def geode(t, y):
    X = y[:3, :]
    Xdot = y[3:, :]
    Xdotdot = zeros_like(X)
    epsilon = 1e-8  # to avoid divide-by-zero

    for i in range(X.shape[1]):
        x, y_, z = X[:, i]
        nablaF = gradF(x, y_, z)
        hessian = HF(x, y_, z)
        num = Xdot[:, i] @ hessian @ Xdot[:, i]
        den = sum(nablaF**2) + epsilon
        Xdotdot[:, i] = -num / den * nablaF

    return vstack((Xdot, Xdotdot))

# Solve the BVP
u = solve_bvp(geode, bc, t_vals, y_guess, tol=1e-5, max_nodes=5000)
assert u.success

# Evaluate the solution
sol = u.sol(linspace(0, 1, 100))
positions = sol[:3, :]
differences = diff(positions, axis=1)
distances = sqrt(sum(differences**2, axis=0))
length_interpolated = sum(distances)

# Output some surface values for debug or analysis
print(f(3, 0), f(-3, 0))

# Visualization
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
x = linspace(-5, 5, 100)
y = linspace(-5, 5, 100)
X, Y = meshgrid(x, y)
Z = f(X, Y)

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(0, 5)

ax.plot_surface(X, Y, Z, alpha=0.4, cmap='viridis')
ax.plot(sol[0], sol[1], sol[2], color='crimson')
ax.set_title("Geodesic on the Gaussian Surface")
plt.show()