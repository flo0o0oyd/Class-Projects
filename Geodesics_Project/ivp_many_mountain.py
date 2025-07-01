from numpy import *
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the "Lonely Mountain" surface f(x, y)
def f(x, y):
    return sin(x) * cos(y) / (1 + 0.02 * x**2 + 0.03 * y**2)

# Gradient of f(x, y)
def gradF(x, y, z):
    Fx = cos(y) * ((0.02*x**2 + 0.03*y**2 + 1) * cos(x) - 0.04*x*sin(x)) / (0.02*x**2 + 0.03*y**2 + 1)**2
    Fy = -(100/3) * sin(x) * ((3/2 * x**2 + y**2 + 100/3) * sin(y) + 2 * y * cos(y)) / (2/3 * x**2 + y**2 +100/3)**2
    Fz = -1
    return stack((Fx, Fy, Fz))

# Hessian matrix of f(x, y) (second partial derivatives)
def HF(x, y, z):
    Fxx = -sin(x) * cos(y) / (1 + 0.02 * x**2 + 0.03 * y**2) - \
          0.04 * f(x, y) / (1 + 0.02 * x**2 + 0.03 * y**2) + \
          0.0016 * x**2 * f(x, y) / (1 + 0.02 * x**2 + 0.03 * y**2)
    Fxy = -cos(x) * sin(y) / (1 + 0.02 * x**2 + 0.03 * y**2) + \
          0.0024 * x * y * f(x, y) / (1 + 0.02 * x**2 + 0.03 * y**2)
    Fyy = -sin(x) * cos(y) / (1 + 0.02 * x**2 + 0.03 * y**2) - \
          0.06 * f(x, y) / (1 + 0.02 * x**2 + 0.03 * y**2) + \
          0.0036 * y**2 * f(x, y) / (1 + 0.02 * x**2 + 0.03 * y**2)
    return array([[Fxx, Fxy, 0], [Fxy, Fyy, 0], [0, 0, 0]])

# Geodesic computation
def my_geodesic(gradF, HF, ip, iv, distance):
    # Correction of initial velocity to make sure it follows the surface and is unit length
    gradient = gradF(ip[0], ip[1], ip[2])
    iv = iv - dot(gradient, iv) * gradient / dot(gradient, gradient)
    iv = iv / sqrt(sum(iv**2))  # Normalize the velocity

    # ODE setup and solve
    def geode(t, y):
        X = y[:3]
        Xdot = y[3:]
        nablaF = gradF(X[0], X[1], X[2])
        hessian = HF(X[0], X[1], X[2])
        num = (Xdot[None, :] * hessian * Xdot[:, None]).sum()
        den = dot(nablaF, nablaF)
        Xdotdot = - num / den * nablaF
        return hstack((Xdot, Xdotdot))

    ic = hstack((ip, iv))
    u = solve_ivp(geode, [0, distance], ic, dense_output=True, rtol=1e-10, atol=1e-10)
    assert u.success
    yy = u.sol(linspace(0, distance, 1000))
    return yy

# Control
ip = array([0, 0, f(0, 0)])  # Initial position on the surface
iv = array([1, 1, 0])  # Initial velocity
distance = 15 * pi  # Length of path to compute

yy = my_geodesic(gradF, HF, ip, iv, distance)

# Visualization
ax = plt.figure().add_subplot(projection='3d')
x = linspace(-10, 10, 100)
y = linspace(-10, 10, 100)
X, Y = meshgrid(x, y)
Z = f(X, Y)  # Calculate surface heights
ax.plot_surface(X, Y, Z, alpha=0.2, cmap='viridis')  # Lonely Mountain surface
ax.plot(yy[0, :], yy[1, :], yy[2, :], lw=2, color="C3")  # The geodesic path
ax.set_title("Geodesic on the Lonely Mountain Surface")
plt.show()

