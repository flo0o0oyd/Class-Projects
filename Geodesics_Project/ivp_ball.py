# This script computes and visualizes a geodesic path on a sphere
# defined by the level surface F(x, y, z) = x² + y² + z² = 9.
# Given an initial point and velocity, it solves a geodesic ODE
# constrained to the surface using a projection method.

from numpy import *
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Scalar surface function defining the sphere
def F(x, y, z):
    return x**2 + y**2 + z**2

# Gradient of the surface function
def gradF(x, y, z):
    return stack((2*x, 2*y, 2*z))

# Hessian (second derivative matrix) of the surface function
def HF(x, y, z):
    return array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])

# Solves the geodesic ODE given initial position, velocity, and arc length
def my_geodesic(gradF, HF, ip, iv, distance):
    # Project initial velocity to tangent space and normalize
    gradient = gradF(*ip)
    iv -= dot(gradient, iv) * gradient / dot(gradient, gradient)
    iv /= sqrt(sum(iv**2))

    # Define geodesic ODE system
    def geode(t, y):
        X = y[:3]
        Xdot = y[3:]
        nablaF = gradF(*X)
        hessian = HF(*X)
        num = (Xdot[None, :] * hessian * Xdot[:, None]).sum()
        den = dot(nablaF, nablaF)
        Xdotdot = -num / den * nablaF
        return hstack((Xdot, Xdotdot))

    # Initial condition: position + velocity
    ic = hstack((ip, iv))
    u = solve_ivp(geode, [0, distance], ic, dense_output=True, rtol=1e-10, atol=1e-10)
    assert u.success
    return u.sol(linspace(0, distance, 1000))

# Example input: start point, velocity, arc length
ip = array([0, 2, sqrt(5)], dtype=float)     # Ensure float type
iv = array([1, 2, 3], dtype=float)           # Arbitrary initial velocity vector
distance = 7 * pi               # Total geodesic path length to trace

# Compute the geodesic path
yy = my_geodesic(gradF, HF, ip, iv, distance)

# Plot the sphere and the computed geodesic path
ax = plt.figure().add_subplot(projection='3d')
theta = linspace(0, 2*pi, 100)
phi = linspace(0, pi, 100)
x = 3 * outer(cos(theta), sin(phi))  # Sphere x-coordinates
y = 3 * outer(sin(theta), sin(phi))  # Sphere y-coordinates
z = 3 * outer(ones(theta.size), cos(phi))  # Sphere z-coordinates

ax.plot_surface(x, y, z, alpha=0.2)                      # Draw the sphere
ax.plot(yy[0, :], yy[1, :], yy[2, :], lw=2, color="C3")  # Draw the geodesic path
ax.set_aspect('equal')
ax.set_title("Geodesic on a Sphere")
plt.show()
