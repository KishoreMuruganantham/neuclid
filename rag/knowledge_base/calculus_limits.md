# Calculus: Limits

## Standard Limits
- lim(x->0) sin(x)/x = 1
- lim(x->0) (1 - cos(x))/x^2 = 1/2
- lim(x->0) tan(x)/x = 1
- lim(x->0) (e^x - 1)/x = 1
- lim(x->0) ln(1+x)/x = 1
- lim(x->0) (a^x - 1)/x = ln(a)
- lim(x->0) (1+x)^(1/x) = e
- lim(n->inf) (1 + 1/n)^n = e

## L'Hopital's Rule
If lim f(x)/g(x) gives 0/0 or inf/inf form:
lim f(x)/g(x) = lim f'(x)/g'(x)
Can be applied repeatedly if the result is still indeterminate.

## Indeterminate Forms
0/0, inf/inf, 0*inf, inf-inf, 0^0, 1^inf, inf^0
Convert all forms to 0/0 or inf/inf before applying L'Hopital.

## For 1^inf form:
lim f(x)^g(x) = e^(lim g(x)*(f(x)-1))

## Squeeze Theorem (Sandwich Theorem)
If g(x) <= f(x) <= h(x) near a point, and lim g(x) = lim h(x) = L,
then lim f(x) = L.
Common use: bounding sin/cos which oscillate between -1 and 1.
Example: lim(x->0) x^2 * sin(1/x) = 0 (since -x^2 <= x^2*sin(1/x) <= x^2)

## Continuity
f is continuous at a if: lim(x->a) f(x) = f(a)
Types of discontinuity: removable, jump, infinite, oscillatory.

## Common Pitfalls
- Do NOT cancel terms that might be zero without checking
- Check left-hand and right-hand limits separately for piecewise functions
- For limits at infinity, divide by the highest power in the denominator
