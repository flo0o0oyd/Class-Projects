from numpy import *
from scipy.integrate import solve_bvp, simpson
import matplotlib.pyplot as plt

# Function definitions
def F(x, y, z):
    return x ** 2 + y ** 2 + z ** 2 - R ** 2

def gradF(x, y, z):
    return 2 * array([x, y, z])

def HF(x, y, z):
    return [[2, 0, 0], [0, 2, 0], [0, 0, 2]]

# Constants and initial conditions
R = 3.0
x1, y1, z1 = 0.0, 3.0, 0.0
x2, y2, z2 = 0.0, -3.0, 0.0

ya = hstack((array([x1, y1, z1])))
yb = array([x2, y2, z2])

def bc(ya, yb):
    return array([
        ya[0] - x1,
        ya[1] - y1,
        ya[2] - z1,
        yb[0] - x2,
        yb[1] - y2,
        yb[2] - z2,
    ])

x = linspace(0, 1, 100)
y = zeros((6, len(x)))

theta = linspace(0, pi, len(x))
y[:3, :] = vstack((
    R * cos(theta),
    R * sin(theta),
    zeros_like(theta)
))

def geode(t, y):
    X = y[:3, :]  # Positions
    Xdot = y[3:, :]  # Velocities
    Xdotdot = zeros_like(X)  # Accelerations
    epsilon = 1e-8

    for i in range(X.shape[1]):
        x, y, z = X[:, i]
        hessian = HF(x, y, z)
        nablaF = gradF(x, y, z)
        num = Xdot[:, i] @ hessian @ Xdot[:, i]
        den = sum(nablaF ** 2) + epsilon
        Xdotdot[:, i] = -num / den * nablaF

    return vstack((Xdot, Xdotdot))

# Solving the boundary value problem
u = solve_bvp(geode, bc, x, y, tol=1e-5, max_nodes=5000)

# Extract the solution
sol = u.sol(x)

# Extract velocity components from the solution
velocity = sol[3:, :]  # dx/dt, dy/dt, dz/dt
speed = sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)  # |v|

# Integrate speed over the parameter range [0, 1] to calculate the length
length = simpson(speed)  # Numerical integration using Simpson's rule
print(length)
