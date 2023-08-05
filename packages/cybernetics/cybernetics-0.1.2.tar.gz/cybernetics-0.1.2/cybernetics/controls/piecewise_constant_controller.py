from typing import Union, List

import numpy as np


Points = Union[List, np.ndarray]


class PiecewiseConstantController:

    def __init__(self,
                 time_grid: Points,
                 values: Points,
                 default_value: float = None):
        self._time_grid = list(time_grid)
        self._values = values
        self._default_value = default_value

    def generate(self, t: float) -> float:
        for i, t_prev in enumerate(self._time_grid[:-1]):
            if t_prev <= t < self._time_grid[i + 1]:
                return self._values[i]
        if self._default_value is None:
            raise ValueError(f"Can not generate control for tau <{t}>")
        else:
            return self._default_value

    def __call__(self, *args, **kwargs):
        return self.generate(kwargs.get("t", args[0]))
