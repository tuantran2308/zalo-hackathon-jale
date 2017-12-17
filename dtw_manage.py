from state import Gesture
from dtw import dtw
import numpy as np
import math

class DTWMANAGER:
    @staticmethod
    def cal_dtw(examplar , cur_gesture):
        def my_custom_norm(x, y):
            return math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2) + math.pow(x[2] - y[2], 2))
        dist, cost, acc, path = dtw(np.array(examplar).reshape(-1,3), np.array(cur_gesture).reshape(-1,3), dist=lambda x, y: my_custom_norm(x,y))
        return dist

