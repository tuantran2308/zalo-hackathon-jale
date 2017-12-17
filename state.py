import math;
import constant;

class Gesture:
    acc = []
    gyr = []

    def copy(self, gesture):
        acc = list(gesture.acc)
        gyr = list(gesture.gyr)

    def add_acc_step(self, a):
        self.acc.append(a)

    def add_gyr_step(self, g):
        self.gyr.append(g)

    def add_acc_to_ind(self, a, ind):
        self.acc[ind]+=a
