import numpy as np
import math

def smoothstep_n(x, k=1):
    x = np.clip(x, 0, 1)
    y = np.zeros_like(x, dtype=float)

    for n in range(k+1):
        coeff = ((-1)**n *
                 math.comb(k+n, n) *
                 math.comb(2*k+1, k-n))
        y += coeff * x**(k+n+1)

    return y