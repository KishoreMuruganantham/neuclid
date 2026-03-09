# Calculus: Optimization

## General Strategy
1. Identify the quantity to optimize (maximize or minimize)
2. Express it as a function of ONE variable
3. Find the domain (constraints on the variable)
4. Take the derivative and set it equal to zero
5. Test critical points (second derivative or endpoint check)
6. Verify the answer makes physical sense

## Common Optimization Problems (JEE)
### Maximum Area
- Rectangle inscribed in a circle of radius r: max area = 2r^2 (square)
- Rectangle inscribed under a curve: set up A = 2x*f(x), solve A'=0

### Minimum Distance
- Distance from point (a,b) to curve y=f(x): minimize D^2 = (x-a)^2 + (f(x)-b)^2
- Minimizing D^2 is equivalent to minimizing D (avoids square root)

### Related Rates
- Differentiate the constraint equation with respect to time
- Substitute known rates and solve for the unknown rate

## Lagrange Multipliers (for constrained optimization)
To optimize f(x,y) subject to g(x,y) = c:
Solve: grad(f) = lambda * grad(g) and g(x,y) = c

## Important Inequalities for Optimization
- AM >= GM: useful for finding min of sum when product is fixed
- For positive a,b: a + b >= 2*sqrt(ab), equality when a = b
- For positive numbers with fixed sum, product is maximized when all are equal

## Common Pitfalls
- Forgetting to check endpoints of the domain
- Not verifying that the critical point is actually a max/min (could be inflection)
- Domain errors: x must satisfy physical constraints (lengths > 0, angles in range)
