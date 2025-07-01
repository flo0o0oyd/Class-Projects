from numpy import *
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

f=1/sqrt(2) #f = (a-c)/a

a=1
b=a
c=a-a*f

def F(x, y, z):
    return x**2 / a**2 + y**2 / b**2 + z**2 / c**2 - 1

def findz(x,y):
    return sqrt(1-x ** 2 / a ** 2 - y ** 2 / b ** 2) * c

def gradF(x, y, z):
    Fx = 2 * x / a**2
    Fy = 2 * y / b**2
    Fz = 2 * z / c**2
    return stack((Fx, Fy, Fz))

def HF(x, y, z):
    Fxx = 2 / a**2
    Fxy = 0
    Fxz = 0
    Fyy = 2 / b**2
    Fyz = 0
    Fzz = 2 / c**2
    return array([[Fxx, Fxy, Fxz], [Fxy, Fyy, Fyz], [Fxz, Fyz, Fzz]])

def my_geodesic(gradF, HF, ip, iv, distance):
    gradient = gradF(ip[0], ip[1], ip[2])
    iv = iv - dot(gradient, iv) * gradient / dot(gradient, gradient)
    iv = iv / sqrt(sum(iv**2))

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

ip = array([1,0,findz(1,0)])
iv = array([0,1,1])
gradient = gradF(ip[0], ip[1], ip[2])
iv = iv - dot(gradient, iv) * gradient / dot(gradient, gradient)
iv = iv / sqrt(sum(iv**2))
distance = 80 * pi
print('ip:',ip)
print('real iv:',iv)

#initial angle
'''
u = array([ip[0], ip[1], 1])
dot_product = dot(iv, u)
norm_v = linalg.norm(iv)
norm_u = linalg.norm(u)
cos_theta = dot_product / (norm_v * norm_u)
theta0 = arccos(cos_theta)
angle_in_degrees = degrees(theta0)
print("initial angle(Rad):", theta0)
print("initial angle(deg):", angle_in_degrees)
beta = 1/2*pi-abs(theta)

#parameter latitude
print('parameter latitude is:',beta)
'''

#flattening
print("flattening is:",f)



yy = my_geodesic(gradF, HF, ip, iv, distance)

ax = plt.figure().add_subplot(projection='3d')
theta = linspace(0, 2 * pi, 100)
phi = linspace(0, pi, 100)
x = a * outer(cos(theta), sin(phi))
y = b * outer(sin(theta), sin(phi))
z = c * outer(ones(theta.size), cos(phi))
ax.plot_surface(x, y, z, alpha=0.2)
ax.plot(yy[0, :], yy[1, :], yy[2, :], lw=1.5, color="C3")
ax.plot(sin(theta), cos(theta), 0, lw=2, color="black")
ax.scatter(ip[0],ip[1],ip[2], color="green", s=50,alpha=1)
ax.quiver(ip[0],ip[1],ip[2],
          iv[0], iv[1], iv[2],
          color='blue', length=1/3, normalize=True)
ax.set_aspect('auto')
ax.set_title("Geodesic on an ellipsoid")
plt.show()
