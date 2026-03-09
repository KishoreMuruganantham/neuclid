# Probability

## Basic Probability
P(A) = favorable outcomes / total outcomes
0 <= P(A) <= 1
P(A') = 1 - P(A)

## Addition Rule
P(A or B) = P(A) + P(B) - P(A and B)
If mutually exclusive: P(A or B) = P(A) + P(B)

## Conditional Probability
P(A|B) = P(A and B) / P(B)
Independence: P(A and B) = P(A) * P(B) iff A and B are independent

## Bayes' Theorem
P(A|B) = P(B|A) * P(A) / P(B)
P(B) = P(B|A)*P(A) + P(B|A')*P(A') (total probability)

## Permutations and Combinations
nPr = n! / (n-r)!
nCr = n! / (r! * (n-r)!)
nCr = nC(n-r)

## Important Identities
- nC0 + nC1 + ... + nCn = 2^n
- nCr + nC(r-1) = (n+1)Cr (Pascal's identity)

## Distributions
### Binomial Distribution
P(X=k) = nCk * p^k * (1-p)^(n-k)
Mean = np, Variance = np(1-p)

### Poisson Distribution
P(X=k) = (lambda^k * e^(-lambda)) / k!
Mean = Variance = lambda

## Expected Value
E[X] = sum of x_i * P(x_i)
E[aX + b] = a*E[X] + b
Var(X) = E[X^2] - (E[X])^2

## Common JEE Problems
- Drawing balls from bags (with/without replacement)
- Dice problems: use complement for "at least one"
- Cards: 52 cards, 4 suits, 13 ranks each
- Derangements: D_n = n! * sum_{k=0}^{n} (-1)^k / k!
