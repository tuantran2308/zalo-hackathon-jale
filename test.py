from utils import FileTool
from dtw_manage import DTWMANAGER
from process import Process
# list = FileTool.readPickle("lock_all_raw")
# # list = list[:len(list)-4]
# print len(list)
# print list
# FileTool.writePickle("trung_lock_all_raw",list)
#
# trung_lock = FileTool.readPickle("trung_lock_all_raw")
# trung_punch = FileTool.readPickle("trung_punch_all_raw")
# tuan_lock = FileTool.readPickle("tuan_lock_all_raw")
# tuan_punch = FileTool.readPickle("tuan_punch_all_raw")

trung_lock = FileTool.readPickle("processed_trung_lock")
trung_punch = FileTool.readPickle("processed_trung_punch")
tuan_lock = FileTool.readPickle("processed_tuan_lock")
tuan_punch = FileTool.readPickle("processed_tuan_punch")

list = []
list.extend(trung_lock)
list.extend(tuan_lock)
list.extend(trung_punch)
list.extend(tuan_punch[2:])

print len(trung_lock[2:])
print len(trung_punch)
print len(tuan_lock)
print len(tuan_punch)


#
# print trung_lock
#
# array = []
# process = Process()
# for ele1 in tuan_punch:
#     for ele2 in ele1:
#         print ele2
#         process.process_data(ele2)
#     array.append(process.all_gesture)
#     print process.all_gesture
#     process.reset()
#
# FileTool.writePickle("processed_tuan_punch",array)


min = 1000000
min_ind = -1
max = -100000
result = 0
for ind1,ele1 in enumerate(list):
        result = DTWMANAGER.cal_dtw(ele1,tuan_punch[1])
        print result
        if min > result:
            min = result
            min_ind = ind1
        if max < result:
            max = result

print "################"
print min
print min_ind
print max