import datetime
import os
import pickle

import numpy

from .errors import LogTypeError
from .grid import NULL, LOG_EVENT_TYPES, gen, GridLog


def generate_null_array(array: iter, shape: int):
    if len(shape) >= 2:
        *new_shape, dim = shape
        return generate_null_array([array] * dim, new_shape)
    else:
        return [array] * shape[0]


class MultiDimensionalArray:
    def __init__(self, shape: tuple):
        self.shape = shape

        self._data = numpy.array(generate_null_array([None], self.shape))

        # self.log = GridLog(self)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return "<MultiDimensionalArray {}>".format(
            "x".join([str(i) for i in self.shape])
        )

    def collapsed_cells(self):
        return list(self._data)

    def update_cell(self, coordinates: tuple, new_value):
        coordinates = [i - 1 for i in coordinates]

        def recursively_update(array, shape, new_value):
            if len(shape) >= 2:
                a, *b = shape
                array = recursively_update(array[a], b, new_value)
            else:
                array[shape[0]] = new_value
            return array

        self._data = recursively_update(self._data, coordinates, new_value)

    def get_cell(self, coordinates: tuple):
        coordinates = [i - 1 for i in coordinates]

        def search_for_cell(array, shape):
            if len(shape) >= 2:
                a = shape[0]
                shape.pop()
                return search_for_cell(array[a], shape)
            else:
                return array

        cell = search_for_cell(self._data, coordinates)
        return cell if cell is not None else NULL

    def save(self, filename="multiarray1.dat"):
        def non_conflicting_file(file):
            if os.path.exists(file):
                new_file, ext = file.split(".")
                new_file = int("".join([char for char in file if char.isdecimal()])) + 1
                return non_conflicting_file(".".join([new_file, ext]))
            else:
                return file

        name = non_conflicting_file(filename)
        with open(name, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)

    def view_axis(self, axis_number):
        axis_length = self.shape[axis_number]
        target = [0 for i in self.shape]
        for i in range(axis_length):
            target[axis_number] = i
            yield self.get_cell(target)
