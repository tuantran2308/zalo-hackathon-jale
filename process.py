import constant
from convert import ConvertRawData
import math

class Process:

    # def __int__(self,knn):
    #     for i in range(0,5):
    #         self.data_inited.append([0,0,0])
    #     self.knn = knn

    # for moving average filter
    data_inited = []
    current_sum = [0,0,0]
    index_for_old_data = 0
    full = False
    num_to_step = 0

    # all gesture
    all_gesture = []
    current_len = 0
    new_step =False
    in_get_gesture= False
    count_no_gap = 0
    current_gesture = []

    # skip
    skip = 0

    def __init__(self, init_knn):
        for i in range(0,5):
            self.data_inited.append([0,0,0])
        self.knn = init_knn

    # def __init__(self):
    #     for i in range(0,5):
    #         self.data_inited.append([0,0,0])

    def reset(self):
        for i in range(0,5):
            self.data_inited.append([0,0,0])
        self.current_sum = [0,0,0]
        self.index_for_old_data = 0
        self.full = False
        self.num_to_step = 0
        self.all_gesture = []

    def process_data(self,data):
        self.current_sum[0] += data[0] - self.data_inited[self.index_for_old_data][0]
        self.current_sum[1] += data[1] - self.data_inited[self.index_for_old_data][1]
        self.current_sum[2] += data[2] - self.data_inited[self.index_for_old_data][2]
        self.data_inited[self.index_for_old_data][0] = data[0]
        self.data_inited[self.index_for_old_data][1] = data[1]
        self.data_inited[self.index_for_old_data][2] = data[2]
        self.index_for_old_data = (self.index_for_old_data+1) % constant.MIN_LENGTH_GESTURE
        # self.full = True
        if (self.index_for_old_data >= constant.MIN_LENGTH_GESTURE-1):
            self.full = True
        self.num_to_step +=1
        if self.num_to_step >= constant.NEXT_STEP_COUNT and self.full:
            self.num_to_step = 0
            acclStep = []
            # acclStep.append(ConvertRawData.quantizeAccelerometerValue(self.current_sum[0]/float(constant.MIN_LENGTH_GESTURE)))
            # acclStep.append(ConvertRawData.quantizeAccelerometerValue(self.current_sum[1]/float(constant.MIN_LENGTH_GESTURE)))
            # acclStep.append(ConvertRawData.quantizeAccelerometerValue(self.current_sum[2]/float(constant.MIN_LENGTH_GESTURE)))

            acclStep.append(self.current_sum[0]/float(constant.MIN_LENGTH_GESTURE))
            acclStep.append(self.current_sum[1]/float(constant.MIN_LENGTH_GESTURE))
            acclStep.append(self.current_sum[2]/float(constant.MIN_LENGTH_GESTURE))
            self.all_gesture.append(acclStep)
            self.new_step = True

            if len(self.all_gesture) > 100:
                del self.all_gesture[0]
            # if len(self.current_len) > constant.CONTINUOUS_3:
            #     type = self.__get_knn_continuous()
            #     if type != 0:
            #         print "result: %d"%type

    def detect_segment(self):
        if self.new_step:
            self.new_step =False

            # check is in move
            gap = self.__get_mag_gap()
            if len(self.all_gesture) > 2 and gap > constant.GAP_THRESS:
                self.in_get_gesture = True
                print "start"
            elif len(self.all_gesture) > 2:
                if self.in_get_gesture:
                    if gap < constant.GAP_THRES_INTERNAL:
                        self.count_no_gap += 1
                    else:
                        self.count_no_gap = 0
                    if self.count_no_gap > constant.NO_GAP_COUNT_THRESS :
                        print "end"
                        self.count_no_gap = 0
                        self.in_get_gesture = False
                        resultType = self.knn.get_type_of_gestures(self.current_gesture)
                        self.current_gesture = []
                
                        return resultType

            # if in move add to current gesture
            if self.in_get_gesture:
                self.current_gesture.append(self.all_gesture[-1])
        return None     

    def __get_mag_gap(self):
        prev_ind = len(self.all_gesture) - 2
        cur_mag = math.sqrt(math.pow(self.all_gesture[-1][0], 2) + math.pow(self.all_gesture[-1][1], 2) + math.pow(self.all_gesture[-1][2], 2))
        prev_mag = math.sqrt(math.pow(self.all_gesture[prev_ind][0], 2) + math.pow(self.all_gesture[prev_ind][1], 2) + math.pow(self.all_gesture[prev_ind][2], 2))
        return math.fabs(cur_mag - prev_mag)
    #
    # def __get_knn_continuous(self):
    #     current_len = len(self.all_gesture)
    #     type = self.knn.get_type_of_gestures(self.all_gesture[current_len-constant.CONTINUOUS_1:current_len-1])
    #     if  type !=0:
    #         self.skip = constant.CONTINUOUS_1
    #         return type
    #
    #     type = self.knn.get_type_of_gestures(self.all_gesture[current_len-constant.CONTINUOUS_2:current_len-1])
    #     if  type !=0:
    #         self.skip = constant.CONTINUOUS_2
    #         return type
    #
    #     type = self.knn.get_type_of_gestures(self.all_gesture[current_len-constant.CONTINUOUS_3:current_len-1])
    #     if  type !=0:
    #         self.skip = constant.CONTINUOUS_3
    #         return type
    #
    #     return 0