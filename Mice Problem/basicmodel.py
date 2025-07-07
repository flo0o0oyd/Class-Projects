# n-sided Pursuit Curve Simulation
import numpy as np
import matplotlib.pyplot as plt

def create_polygon(n_sides, radius=10):
    """Create regular polygon with n sides centered at the origin."""
    angles = np.linspace(0, 2 * np.pi, n_sides, endpoint=False)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    return np.column_stack((x, y))

def pursuit_simulation(vertices, velocity=0.5, dt=0.1, steps=1000, threshold=0.01):
    """Simulate pursuit motion of polygon vertices towards the next vertex."""
    n = len(vertices)
    trajectory = [vertices.copy()]

    for _ in range(steps):
        new_vertices = vertices.copy()
        for i in range(n):
            target = vertices[(i + 1) % n]
            direction = target - vertices[i]
            norm = np.linalg.norm(direction)
            if norm > 0:
                direction /= norm
                new_vertices[i] += direction * velocity * dt

        vertices = new_vertices
        trajectory.append(vertices.copy())

        # Stop if all points are very close to each other (converged)
        if all(np.linalg.norm(vertices[(i + 1) % n] - vertices[i]) < threshold for i in range(n)):
            break

    return np.array(trajectory)

def plot_trajectory(trajectory, title="Pursuit Polygon Simulation"):
    """Plot the trajectory of the polygon shrinking."""
    plt.figure(figsize=(8, 8))
    for frame in trajectory:
        closed = np.vstack([frame, frame[0]])  # Close the polygon
        plt.plot(closed[:, 0], closed[:, 1], 'k-', alpha=0.1)
    plt.title(title)
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# --- Main Script ---
if __name__ == "__main__":
    try:
        n_sides = int(input("Enter the number of sides for the polygon: "))
        dt = float(input("Enter the time gap (dt): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        exit()

    initial_vertices = create_polygon(n_sides)
    traj = pursuit_simulation(initial_vertices, velocity=0.5, dt=dt, steps=1000)
    plot_trajectory(traj)
