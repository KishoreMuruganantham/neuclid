# Calculus: Derivatives

## Basic Rules
- d/dx [x^n] = n*x^(n-1)
- d/dx [e^x] = e^x
- d/dx [a^x] = a^x * ln(a)
- d/dx [ln(x)] = 1/x
- d/dx [sin(x)] = cos(x)
- d/dx [cos(x)] = -sin(x)
- d/dx [tan(x)] = sec^2(x)

## Product Rule
d/dx [f*g] = f'*g + f*g'

## Quotient Rule
d/dx [f/g] = (f'*g - f*g') / g^2

## Chain Rule
d/dx [f(g(x))] = f'(g(x)) * g'(x)

## Implicit Differentiation
When y is defined implicitly by F(x,y) = 0:
dy/dx = -F_x / F_y (where F_x, F_y are partial derivatives)

## Logarithmic Differentiation
For y = f(x)^g(x):
Take ln of both sides: ln(y) = g(x)*ln(f(x))
Differentiate both sides using chain rule.

## Applications
- Tangent line at (a, f(a)): y - f(a) = f'(a)(x - a)
- Normal line: y - f(a) = -1/f'(a) * (x - a)
- Rate of change: dy/dt = (dy/dx)(dx/dt)
- Rolle's Theorem: If f(a)=f(b), then exists c in (a,b) where f'(c)=0
- Mean Value Theorem: exists c in (a,b) where f'(c) = (f(b)-f(a))/(b-a)

## Maxima and Minima
First derivative test:
- f'(x) changes from + to -: local maximum
- f'(x) changes from - to +: local minimum
Second derivative test:
- f''(c) < 0: local maximum at c
- f''(c) > 0: local minimum at c
- f''(c) = 0: test is inconclusive
