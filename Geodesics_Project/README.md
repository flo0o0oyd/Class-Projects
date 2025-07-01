# 🌀 Geodesics Project

This project numerically computes and visualizes **geodesics** (shortest paths) on curved surfaces using both:

- **Initial Value Problem (IVP)** methods  
- **Boundary Value Problem (BVP)** methods

The surfaces include:
- Gaussian bumps
- Spheres
- Ellipsoids

All paths are visualized in 3D using `matplotlib`.

---

## ✏️ What is a Geodesic?

A **geodesic** is the shortest path between two points on a surface. On a flat plane, it’s a straight line. On a curved surface (like a sphere or a mountain), it bends to follow the surface’s shape.

---

## ⚙️ Two Ways to Compute Geodesics

### 🔹 1. IVP: Initial Value Problem

> “Start at this point, go in this direction — where do you end up?”

- Requires:
  - Initial position
  - Initial velocity (direction)
- Solves an ODE forward in time
- Good when only one end of the path is fixed

### 🔹 2. BVP: Boundary Value Problem

> “I want to go from point A to point B — what's the shortest path on the surface?”

- Requires:
  - Start and end positions
- Solves a two-point boundary value problem (BVP)
- Usually involves nonlinear ODEs with surface constraints
