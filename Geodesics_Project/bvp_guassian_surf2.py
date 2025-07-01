from numpy import *
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

# Surface height function: a Gaussian bump
a = 3
def f(x, y):
    return a * exp(-x**2 - y**2)

# Gradient of the implicit surface F(x, y, z) = f(x, y) - z = 0
def gradF(x, y, z):
    Fx = -2 * x * a * exp(-x**2 - y**2)
    Fy = -2 * y * a * exp(-x**2 - y**2)
    Fz = -1
    return stack((Fx, Fy, Fz))

# Hessian matrix of F
def HF(x, y, z):
    exp_term = exp(-x**2 - y**2)
    Fxx = 2 * a * (2 * x**2 - 1) * exp_term
    Fxy = 4 * a * x * y * exp_term
    Fyy = 2 * a * (2 * y**2 - 1) * exp_term
    return array([[Fxx, Fxy, 0], [Fxy, Fyy, 0], [0, 0, 0]])

# Start and end points on the surface
x1, y1, z1 = 0, -3, f(0, -3)
x2, y2, z2 = 1,  3, f(1,  3)

# Boundary conditions: enforce fixed endpoints
def bc(ya, yb):
    return array([
        ya[0] - x1,
        ya[1] - y1,
        ya[2] - z1,
        yb[0] - x2,
        yb[1] - y2,
        yb[2] - z2
    ])

# Initial guess for path: straight line between endpoints
t_guess = linspace(0, 1, 100)
y_guess = zeros((6, len(t_guess)))
y_guess[:3, :] = linspace([x1, y1, z1], [x2, y2, z2], len(t_guess)).T

# Geodesic ODE system for BVP
def geode(t, y):
    X = y[:3]
    Xdot = y[3:]
    Xdotdot = zeros_like(X)

    for i in range(X.shape[1]):
        x, y_, z = X[:, i]
        nablaF = gradF(x, y_, z)
        hessian = HF(x, y_, z)
        numerator = Xdot[:, i] @ hessian @ Xdot[:, i]
        denominator = sum(nablaF ** 2)
        Xdotdot[:, i] = - numerator / denominator * nablaF

    return vstack((Xdot, Xdotdot))

# Solve the boundary value problem
u = solve_bvp(geode, bc, t_guess, y_guess, tol=1e-5, max_nodes=1000)
assert u.success

# Evaluate solution at finer resolution
n = 100
sol = u.sol(linspace(0, 1, n))

# Plot the surface and geodesic path
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Surface mesh for visualization
x = linspace(-10, 10, 100)
y = linspace(-10, 10, 100)
X, Y = meshgrid(x, y)
Z = f(X, Y)

# Plot the surface and path
ax.plot_surface(X, Y, Z, alpha=0.4, cmap='viridis')
ax.plot(sol[0], sol[1], sol[2], color='crimson', linewidth=2)

ax.set_title("Geodesic on the Gaussian Surface")
ax.set_aspect('auto')
plt.show()
