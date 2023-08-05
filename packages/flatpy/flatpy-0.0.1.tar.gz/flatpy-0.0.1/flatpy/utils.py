import numpy as np


def generate_test_grid_2d(resolution=40):
    """
    """
    x, y = np.mgrid[0:1:(resolution * 1j), 0:1:(resolution * 1j)]
    return np.vstack([x.ravel(), y.ravel()]).T


def unpack2D(_x):
    """
        Helper function for splitting 2D data into x and y component to make
        equations simpler
    """
    _x = np.atleast_2d(_x)
    x = _x[:, 0]
    y = _x[:, 1]
    return x, y

def gaussian_2d(x, mu=0.75, sigma=0.25):
    return np.exp(-sum((x-mu)**2/(2*sigma**2)))

def add_nonuniform_noise(field, noise_level):
    epsilon = np.random.uniform(-noise_level, noise_level, field.shape)
    amplitude = np.ones(field.shape)
    for row in range(amplitude.shape[0]):
        y = row / amplitude.shape[0]
        for col in range(amplitude.shape[1]):
            x = col / amplitude.shape[1]
            amplitude[row, col] = gaussian_2d(np.array([x, y]))
    return field + amplitude*epsilon

def add_uniform_noise(field, noise_level):
    epsilon = np.random.uniform(-noise_level, noise_level, field.shape)
    return field + epsilon