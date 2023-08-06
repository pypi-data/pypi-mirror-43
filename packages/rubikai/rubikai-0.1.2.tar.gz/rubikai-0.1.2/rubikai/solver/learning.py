import numpy as np
from rubikai.cube.cube import Cube
from rubikai.solver.solver import generate_random_sequence


def scrambled_cube_generator(layers, max_d, p=None):
    """
    a generator that performs a random walk _back_ from a solved cube, where
    the number of moves performed is at most `max_d' (inclusive).
    yields a pair of a scrambled_cube_array and the number of actual moves
    performed.
    :param layers: the number of layers in the scrambled cube
    :param max_d: the maximal depth of the random walk
    :param p: (optional) a length (max_d+1) probabilities vector according to
              which the number of scramble-steps is chosen.
    :return: (arr, d) pairs, where `arr' is a scrambled-cube array and d is
              the number of moves that were performed to scramble it.
    """
    d_values = np.arange(max_d + 1)
    while True:
        cube = Cube(layers)
        d = np.random.choice(d_values, p=p)
        actions = generate_random_sequence(layers, d)
        cube.apply(actions)
        yield cube.to_array(), d


def batch_generator(layers, max_d, batch_size, p=None):
    """
    same as `scrambled_cube_generator', but for batches of data.
    :param layers: cube dimension (layers x layers x layers cube)
    :param max_d: maximal number of scramble-steps
    :param batch_size: number of instances for each iteration
    :param p: num-of-steps probabilities vector (see scrambled_cube_generator)
    :return: (data, labels) pair, where `data' is a 2d array in which each row
              is a scrambled cube array. labels is a 1d array where each entry
              corresponds to a row in the data array.
    """
    dimension = len(Cube(layers).to_array())
    while True:
        # preallocate the output arrays
        data = np.empty((batch_size, dimension), dtype=np.int8)
        labels = np.empty(batch_size, dtype=np.int8)
        # generate instances until batch_size is reached
        for i, (arr, d) in enumerate(
                scrambled_cube_generator(layers, max_d, p)):
            if i >= batch_size:
                break
            data[i, :] = arr
            labels[i] = d
        yield data, labels
