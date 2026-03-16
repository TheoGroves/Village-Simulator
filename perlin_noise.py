import math
import random

p = list(range(256))
random.shuffle(p)
p = p * 2


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(a, b, t):
    return a + t * (b - a)


def grad(hash, x, y, z):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else (x if h in (12, 14) else z)
    return ((u if (h & 1) == 0 else -u) +
            (v if (h & 2) == 0 else -v))


def perlin(x, y, z):
    X = int(math.floor(x)) & 255
    Y = int(math.floor(y)) & 255
    Z = int(math.floor(z)) & 255

    x -= math.floor(x)
    y -= math.floor(y)
    z -= math.floor(z)

    u = fade(x)
    v = fade(y)
    w = fade(z)

    A = p[X] + Y
    AA = p[A] + Z
    AB = p[A + 1] + Z
    B = p[X + 1] + Y
    BA = p[B] + Z
    BB = p[B + 1] + Z

    res = lerp(
        lerp(
            lerp(grad(p[AA], x, y, z),
                 grad(p[BA], x - 1, y, z), u),
            lerp(grad(p[AB], x, y - 1, z),
                 grad(p[BB], x - 1, y - 1, z), u),
            v
        ),
        lerp(
            lerp(grad(p[AA + 1], x, y, z - 1),
                 grad(p[BA + 1], x - 1, y, z - 1), u),
            lerp(grad(p[AB + 1], x, y - 1, z - 1),
                 grad(p[BB + 1], x - 1, y - 1, z - 1), u),
            v
        ),
        w
    )

    return (res + 1) / 2 # converts -1-1 -> 0-1


def perlin_octaves(x, y, z, octaves=8, persistence=0.5, lacunarity=2.0):
    frequency = 1.0
    amplitude = 1.0
    
    total = 0.0
    max_value = 0.0

    for octave in range(octaves):
        value = perlin(x * frequency, y * frequency, z * frequency)

        total += value * amplitude
        max_value += amplitude

        frequency *= lacunarity
        amplitude *= persistence

    return total / max_value