from utils import FileTool
from dtw_manage import DTWMANAGER
from process import Process

trung_lock = FileTool.readPickle("trung_lock_all_raw")
trung_punch = FileTool.readPickle("trung_punch_all_raw")
trung_unlock = FileTool.readPickle("trung_unlock_all_raw")
trung_hook = FileTool.readPickle("trung_hook_all_raw")
trung_next = FileTool.readPickle("trung_next_all_raw")
trung_prev = FileTool.readPickle("trung_prev_all_raw")
tuan_lock = FileTool.readPickle("tuan_lock_all_raw")
tuan_punch = FileTool.readPickle("tuan_punch_all_raw")
tuan_unlock = FileTool.readPickle("tuan_unlock_all_raw")
tuan_hook = FileTool.readPickle("tuan_hook_all_raw")
tuan_next = FileTool.readPickle("tuan_next_all_raw")
tuan_prev = FileTool.readPickle("tuan_prev_all_raw")


print len(trung_prev)

array = []
process = Process()
for ele1 in tuan_prev:
    for ele2 in ele1:
        print ele2
        process.process_data(ele2)
    array.append(process.all_gesture)
    print process.all_gesture
    process.reset()

FileTool.writePickle("processed_tuan_prev",array)
