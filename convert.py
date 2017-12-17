
class ConvertRawData:
    @staticmethod
    def quantizeAccelerometerValue(value):
        if (value > 2):
            return 16
        elif (value <= 2 and value > 1):
            return int((value - 1) / 0.2) + 1
        elif (value <= 1 and value > 0):
            return int(value / 0.1) + 1
        elif (value == 0):
            return 0
        elif (value < 0 and value >= -1):
            return int(value / 0.1) - 1;
        elif (value >= -2 and value < -1):
            return int((value + 1) / 0.2) - 1;
        else:
            return -16;
