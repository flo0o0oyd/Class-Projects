from numpy import *
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

# Ellipsoid parameters
a, b, c = 3, 2, 1

# Implicit surface function F(x, y, z) = 0
def F(x, y, z):
    return x**2 / a**2 + y**2 / b**2 + z**2 / c**2 - 1

# Given x, y on surface, solve for positive z
def findz(x, y):
    return sqrt(1 - x**2 / a**2 - y**2 / b**2) * c

# Gradient of F
def gradF(x, y, z):
    Fx = 2 * x / a**2
    Fy = 2 * y / b**2
    Fz = 2 * z / c**2
    return stack((Fx, Fy, Fz))

# Hessian of F
def HF(x, y, z):
    return array([
        [2 / a**2, 0,         0],
        [0,        2 / b**2,  0],
        [0,        0,         2 / c**2]
    ])

# Two endpoints on the ellipsoid
x1, y1, z1 = 0.5, 0.5, findz(0.5, 0.5)
x2, y2, z2 = 1.0, 1.0, findz(1.0, 1.0)

# Boundary conditions: fix endpoints
def bc(ya, yb):
    return array([
        ya[0] - x1, ya[1] - y1, ya[2] - z1,
        yb[0] - x2, yb[1] - y2, yb[2] - z2
    ])

# Initial guess: semicircular path
R = 3.0
t_vals = linspace(0, 1, 100)
theta = linspace(0, pi, len(t_vals))

y_guess = zeros((6, len(t_vals)))
y_guess[:3, :] = vstack((
    R * cos(theta),
    R * sin(theta),
    zeros_like(theta)
))

# Geodesic equation
def geode(t, y):
    X = y[:3, :]
    Xdot = y[3:, :]
    Xdotdot = zeros_like(X)
    epsilon = 1e-8

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

# Evaluate solution
sol = u.sol(linspace(0, 1, 100))
positions = sol[:3, :]
differences = diff(positions, axis=1)
distances = sqrt(sum(differences**2, axis=0))
length_interpolated = sum(distances)

# Output results
print("Path length:", length_interpolated)
print("Endpoints:", (x1, y1, z1), "to", (x2, y2, z2))

# Plot the ellipsoid and geodesic
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Ellipsoid surface mesh
theta = linspace(0, 2*pi, 100)
phi = linspace(0, pi, 100)
X = a * outer(cos(theta), sin(phi))
Y = b * outer(sin(theta), sin(phi))
Z = c * outer(ones(theta.size), cos(phi))
ax.plot_surface(X, Y, Z, alpha=0.2, cmap='viridis')

# Plot geodesic
ax.plot(sol[0], sol[1], sol[2], color='crimson')
ax.set_title("Geodesic on an Ellipsoid")
ax.set_aspect('auto')
plt.show()
