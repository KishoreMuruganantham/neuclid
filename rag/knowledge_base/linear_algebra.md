# Linear Algebra Basics

## Matrices
Addition: A + B (element-wise, same dimensions)
Scalar multiplication: cA (multiply each element by c)
Matrix multiplication: (AB)_ij = sum_k A_ik * B_kj
Dimensions: (m x n) * (n x p) = (m x p)

## Determinants
2x2: det([[a,b],[c,d]]) = ad - bc
3x3: Expand along any row/column using cofactors
Properties:
- det(AB) = det(A) * det(B)
- det(A^T) = det(A)
- det(kA) = k^n * det(A) for n x n matrix
- If any row/column is all zeros, det = 0
- Swapping two rows changes sign of det
- If two rows are identical, det = 0

## Inverse of a Matrix
A^(-1) exists iff det(A) != 0
For 2x2: A^(-1) = (1/det(A)) * [[d,-b],[-c,a]]
AA^(-1) = A^(-1)A = I
(AB)^(-1) = B^(-1) * A^(-1)

## Systems of Linear Equations (Ax = b)
- Unique solution: det(A) != 0
- No solution or infinite solutions: det(A) = 0
- Cramer's Rule: x_i = det(A_i) / det(A)

## Eigenvalues and Eigenvectors
Av = lambda * v
Characteristic equation: det(A - lambda*I) = 0
Sum of eigenvalues = trace(A)
Product of eigenvalues = det(A)

## Rank
rank(A) = number of non-zero rows after row echelon form
rank(A) <= min(m, n)
For Ax = b: consistent iff rank(A) = rank([A|b])

## Common Pitfalls
- Matrix multiplication is NOT commutative: AB != BA in general
- det(A+B) != det(A) + det(B)
- (A+B)^2 != A^2 + 2AB + B^2 (unless AB = BA)
