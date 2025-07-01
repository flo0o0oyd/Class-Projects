import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp
from mpl_toolkits.mplot3d import Axes3D

def testtt(x1, y1):
    a = 2

    def f(x, y):
        return a * np.e ** (-x ** 2 - y ** 2)

    z1 = f(x1, y1)

    def gradF(x, y, z):
        Fx = -2 * x * a * np.e ** (-x ** 2 - y ** 2)
        Fy = -2 * y * a * np.e ** (-x ** 2 - y ** 2)
        Fz = -1
        return np.array([Fx, Fy, Fz])

    def HF(x, y, z):
        Fxx = 2 * a * (2 * x ** 2 - 1) * np.e ** (-x ** 2 - y ** 2)
        Fxy = 4 * a * x * y * np.e ** (-x ** 2 - y ** 2)
        Fyy = 2 * a * (2 * y ** 2 - 1) * np.e ** (-x ** 2 - y ** 2)
        return np.array([[Fxx, Fxy, 0], [Fxy, Fyy, 0], [0, 0, 0]])

    R = 3.0
    x2, y2, z2 = -5.0, -5.0, f(-5, -5)

    def bc(ya, yb):
        return np.array([
            ya[0] - x1,
            ya[1] - y1,
            ya[2] - z1,
            yb[0] - x2,
            yb[1] - y2,
            yb[2] - z2
        ])

    x = np.linspace(0, 1, 100)
    y = np.zeros((6, len(x)))
    theta = np.linspace(0, np.pi, len(x))
    y[:3, :] = np.vstack((
        R * np.cos(theta),
        R * np.sin(theta),
        np.zeros_like(theta)
    ))

    def geode(t, y):
        X = y[:3, :]
        Xdot = y[3:, :]
        Xdotdot = np.zeros_like(X)
        epsilon = 1e-8
        for i in range(X.shape[1]):
            x, y, z = X[:, i]
            hessian = HF(x, y, z)
            nablaF = gradF(x, y, z)
            num = Xdot[:, i] @ hessian @ Xdot[:, i]
            den = np.sum(nablaF ** 2) + epsilon
            Xdotdot[:, i] = -num / den * nablaF
        return np.vstack((Xdot, Xdotdot))

    u = solve_bvp(geode, bc, x, y, tol=1e-5, max_nodes=5000)
    if not u.success:
        return np.nan  # 如果 BVP 失败，返回 NaN
    sol = u.sol(np.linspace(0, 1, 100))
    z_vals = sol[2]
    max_idx = max(z_vals)
    positions = sol[:3, :]
    differences = np.diff(positions, axis=1)
    distances = np.sqrt(np.sum(differences ** 2, axis=0))
    length_interpolated = np.sum(distances)
    #print(max(z_vals))
    return max_idx

x = np.linspace(-5, 5, 30)
y = np.linspace(-5, 5, 30)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i, j] = testtt(X[i, j], Y[i, j])

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_title('Heightest point in the geodesics between the location and (-5,-5,0), when a=2')
plt.show()
