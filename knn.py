from dtw_manage import DTWMANAGER
import constant

name = ["lock","punch","unlock","hook",'next','prev']

class KNN:
    trained_data = []

    def load_file(self,list):
        self.trained_data = list

    def get_type_of_gestures(self, cur_state):
        # print cur_state
        type = -1
        min = 100000000

        for index,ele in enumerate(self.trained_data):
            dtwScore = DTWMANAGER.cal_dtw(ele,cur_state)
            if (min > dtwScore):
                min = dtwScore;
                type = index

        print "Min value: %f"%min
        if (min < constant.THRESHOLDOFREALGESTURE):
            print "Type : %s" % name[int(type / 60.0)]
            return name[int(type / 60.0)]
        else:
            print "Wtf r u doing ?"
            return -1
        return type
