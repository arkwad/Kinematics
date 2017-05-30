# ==========================================================
#   File : lagrange.py
#   Author: Arkadiusz Wadowski
#   Email: wadowski.arkadiusz@gmail.com
#   Created: 30.05.2017
# ==========================================================

from sympy import *


l1 = 1.4    # [m]
l2 = 0.85   # [m]
m1 = 1.4    # [kg]
m2 = 3.2    # [kg]
g = 9.81    # [m/s^2]

th1, th2, dth1, dth2, ddth1, ddth2, dx1, dy1, dx2, dy2, v1, v2 = symbols('th1 th2 dth1 dth2 ddth1 ddth2 dx1 dy1 dx2 dy2 v1 v2')
Ek1, Ek2, Ek, Ep1, Ep2, Ep, L, tau1, tau2 = symbols('Ek1 Ek2 Ek Ep1 Ep2 Ep L tau1 tau2')

#calculation of v1
dx1 = -l1/2 *sin(th1)*dth1
dy1 = -l1/2 *cos(th1)*dth1

v1 = simplify(sqrt(dx1 **2 + dy1 ** 2))

# calculations of v2
dx2 = -l1/2 *sin(th1)*dth1 - l1/2 *sin(th2)*dth2
dy2 = -l1/2 *cos(th1)*dth1 - l1/2 *cos(th2)*dth2
v2 = simplify( sqrt(dx2 ** 2 + dy2 ** 2) )

# calculations of Kinematic Energy
Ek1 = simplify( 0.5 * m1 * v1 ** 2 )
Ek2 = simplify( 0.5 * m2 * v2 ** 2 )
Ek = Ek1 + Ek2

# calculations of Potential Energy

Ep1 = -m1* g* sin(th1)
Ep2 = -m2* g* ( l1 * sin(th1) + l2/2 * sin(th2) )
Ep = Ep1 + Ep2

L = Ek - Ep
print(L)
t = Symbol('t')

tau1 = diff(diff(L, dth1).subs( [(th1, th1(t)), (th2, th2(t)), (dth1, dth1(t)), (dth2, dth2(t)) ] ),t) - diff(L.subs( [(th1, th1(t)), (th2, th2(t)), (dth1, dth1(t)), (dth2, dth2(t)) ] ), th1)
tau1 = tau1.subs([(Derivative(th1(t), t),dth1), (Derivative(th2(t), t),dth2), (Derivative(dth1(t), t),ddth1),(Derivative(dth2(t), t),ddth2)])

tau2 = diff(diff(L, dth2).subs( [(th1, th1(t)), (th2, th2(t)), (dth1, dth1(t)), (dth2, dth2(t)) ] ),t) - diff(L.subs( [(th1, th1(t)), (th2, th2(t)), (dth1, dth1(t)), (dth2, dth2(t)) ] ), th2)
tau2 = tau2.subs([(Derivative(th1(t), t),dth1), (Derivative(th2(t), t),dth2), (Derivative(dth1(t), t),ddth1),(Derivative(dth2(t), t),ddth2)])

print(tau1)
print(tau2)


