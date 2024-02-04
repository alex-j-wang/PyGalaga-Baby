import numpy as np

DIVE_TIME = 100 # Dive duration

with open('resources/x_pattern.txt', 'r') as f:
    x_pattern = f.read().split('\n')

with open('resources/y_pattern.txt', 'r') as f:
    y_pattern = f.read().split('\n')

# Standard factors for the cubic bezier curve
t_range = np.arange(0, 1, 5 / DIVE_TIME)
factor_p0 = (1 - t_range)**3
factor_p1 = 3 * (1 - t_range)**2 * t_range
factor_p2 = 3 * (1 - t_range) * t_range**2
factor_p3 = t_range**3

def cubic_bezier(c0, c1, c2, c3):
    """For a single dimension, returns the cubic bezier
    curve for the given control points."""
    return factor_p0 * c0 + factor_p1 * c1 + factor_p2 * c2 + factor_p3 * c3

def generate_bezier_x(x_conv, end_x):
    """Given the x conversion table, generates the x
    bezier curve for the dive."""
    bezier_x = []
    for i, line in enumerate(x_pattern):
        x_coords = [x_conv[c] for c in line]
        # For final bezier, seek the correct position in the configuration
        if i == 4:
            x_coords[2] = x_coords[3] = end_x
        bezier_x.append(cubic_bezier(*x_coords))
    return np.concatenate(bezier_x)

def generate_bezier_y(y_conv):
    """Given the y conversion table, generates the y
    bezier curve for the dive."""
    bezier_y = []
    for line in y_pattern:
        y0 = y_conv[line[0]] # Initial control y
        o0 = y_conv[line[1]] # Operation applied to y0 to get second control y
        o1 = y_conv[line[2]] # Operation applied to y1 to get third control y
        y1 = y_conv[line[3]] # Final control y
        y_coords = [y0, o0(y0), o1(y1), y1]
        bezier_y.append(cubic_bezier(*y_coords))
    return np.concatenate(bezier_y)