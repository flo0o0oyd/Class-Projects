# This script computes and visualizes a geodesic curve on the surface
# z = f(x, y) = a * exp(-x² - y²), shaped like a Gaussian "Lonely Mountain".
# The geodesic is computed using a projected ODE system derived from
# the surface's gradient and Hessian.

from numpy import *
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

a = 3  # Amplitude of the Gaussian surface

# Surface function: Gaussian bump
def f(x, y):
    return a * exp(-x**2 - y**2)

# Gradient of the surface: returns ∇F = (Fx, Fy, Fz)
def gradF(x, y, z):
    Fx = -2 * x * a * exp(-x**2 - y**2)
    Fy = -2 * y * a * exp(-x**2 - y**2)
    Fz = -1  # Because F(x, y, z) = f(x, y) - z = 0
    return stack((Fx, Fy, Fz))

# Hessian matrix of the surface function
def HF(x, y, z):
    exp_term = exp(-x**2 - y**2)
    Fxx = 2 * a * (2 * x**2 - 1) * exp_term
    Fxy = 4 * a * x * y * exp_term
    Fyy = 2 * a * (2 * y**2 - 1) * exp_term
    return array([
        [Fxx, Fxy, 0],
        [Fxy, Fyy, 0],
        [0,   0,   0]
    ])

# Geodesic solver: returns points along the geodesic
def my_geodesic(gradF, HF, ip, iv, distance):
    # Project initial velocity to the tangent space of the surface and normalize
    gradient = gradF(*ip)
    iv = iv - dot(gradient, iv) * gradient / dot(gradient, gradient)
    iv = iv / sqrt(sum(iv**2))

    # Define the geodesic ODE system
    def geode(t, y):
        X = y[:3]
        Xdot = y[3:]
        nablaF = gradF(*X)
        hessian = HF(*X)
        num = (Xdot[None, :] * hessian * Xdot[:, None]).sum()
        den = dot(nablaF, nablaF)
        Xdotdot = -num / den * nablaF
        return hstack((Xdot, Xdotdot))

    # Solve ODE with given initial condition (position + velocity)
    ic = hstack((ip, iv))
    u = solve_ivp(geode, [0, distance], ic, dense_output=True, rtol=1e-10, atol=1e-10)
    assert u.success
    return u.sol(linspace(0, distance, 1000))

# Set up initial point and velocity
ip = array([-5.0, 0.0, f(-3, 0)])     # Initial point on the surface
iv = array([1.0, 1.0, 0.0])          # Initial velocity (projected later)
distance = 20                        # Arc-length to trace along the geodesic

# Compute the geodesic path
yy = my_geodesic(gradF, HF, ip, iv, distance)

# Plot the surface and the geodesic path
ax = plt.figure().add_subplot(projection='3d')
x = linspace(-10, 10, 100)
y = linspace(-10, 10, 100)
X, Y = meshgrid(x, y)
Z = f(X, Y)  # Gaussian surface values

ax.plot_surface(X, Y, Z, alpha=0.4, cmap='viridis')  # Surface plot
ax.plot(yy[0, :], yy[1, :], yy[2, :], lw=2, color="C3")  # Geodesic path

ax.set_title("Geodesic on the Lonely Mountain Surface")
plt.show()
