from numpy import *
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Surface function, gradient, and Hessian
def F(x, y, z):
    return x**2 + y**2 + z**2

def gradF(x, y, z):
    Fx = 2*x
    Fy = 2*y
    Fz = 2*z
    return stack((Fx, Fy, Fz))

def HF(x, y, z):
    Fxx = 2
    Fxy = Fxz = Fyz = 0
    Fyy = 2
    Fzz = 2
    return array([[Fxx, Fxy, Fxz], [Fxy, Fyy, Fyz], [Fxz, Fyz, Fzz]])

# Geodesic solver with given initial position and velocity
def solve_geodesic(gradF, HF, ip, iv, t_max):
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
    u = solve_ivp(geode, [0, t_max], ic, dense_output=True, rtol=1e-8, atol=1e-8)
    return u

# Main function to compute initial velocity and geodesic distance
def compute_geodesic(gradF, HF, ip, fp):
    # Ensure final point is on the surface
    assert abs(F(fp[0], fp[1], fp[2]) - F(ip[0], ip[1], ip[2])) < 1e-6, "Final point is not on the surface!"

    def objective(iv):
        iv = array(iv) / linalg.norm(iv)  # Ensure unit length
        result = solve_geodesic(gradF, HF, ip, iv, t_max=50.0)  # Increase t_max if needed
        final_pos = result.y[:3, -1]  # Extract final position
        return linalg.norm(final_pos - fp)  # Minimize distance to fp

    # Improved initial guess for velocity
    init_guess = fp - ip
    init_guess = init_guess / linalg.norm(init_guess)  # Normalize

    # Use a robust optimizer
    opt_result = minimize(objective, init_guess, method='Nelder-Mead', options={'maxiter': 1000, 'disp': True})
    assert opt_result.success, f"Optimization failed! Message: {opt_result.message}"

    # Extract optimized initial velocity
    iv_opt = opt_result.x / linalg.norm(opt_result.x)  # Normalize to unit vector

    # Solve the geodesic with optimized velocity to compute distance
    geodesic_result = solve_geodesic(gradF, HF, ip, iv_opt, t_max=50.0)
    path = geodesic_result.y[:3, :]  # Extract the geodesic path
    distance = sum(sqrt(sum(diff(path, axis=1)**2, axis=0)))  # Compute arc length

    return iv_opt, distance, path

# Visualization function
def plot_geodesic(ip, fp, path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the sphere
    theta = linspace(0, 2*pi, 100)
    phi = linspace(0, pi, 100)
    x = 3 * outer(cos(theta), sin(phi))  # Spherical coordinates
    y = 3 * outer(sin(theta), sin(phi))
    z = 3 * outer(ones(theta.size), cos(phi))
    ax.plot_surface(x, y, z, alpha=0.2, color='blue', edgecolor='k')

    # Plot the geodesic path
    ax.plot(path[0, :], path[1, :], path[2, :], color='red', linewidth=2, label="Geodesic Path")

    # Mark initial and final points
    ax.scatter(ip[0], ip[1], ip[2], color='green', s=50, label="Initial Point")
    ax.scatter(fp[0], fp[1], fp[2], color='orange', s=50, label="Final Point")

    # Set labels and aspect ratio
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_aspect('auto')
    ax.set_title("Geodesic on a Sphere")
    ax.legend()
    plt.show()

# Example usage
ip = array([0, 0, 3])  # Initial position
fp = array([0, 3, 0])  # Final position

iv_opt, geodesic_distance, path = compute_geodesic(gradF, HF, ip, fp)

print(f"Optimal initial velocity direction: {iv_opt}")
print(f"Geodesic distance: {geodesic_distance:.6f}")

# Plot the geodesic path
plot_geodesic(ip, fp, path)
