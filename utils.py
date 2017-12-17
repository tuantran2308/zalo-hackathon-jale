import json
import os
import codecs
# import timeout_decorator
# import xlsxwriter
import datetime
import pickle
import random
import time
import sys

class TimeOutRequest(Exception):
    pass


class LimitedAccessToken(Exception):
    pass

class ReLogin(Exception):
    pass

#
# class RunRequestTimeOut:
#     """
#     Handle time out request
#     """
#     max_run_time = 3
#     wait_time = 60
#     num_run = 0
#
#
#     @staticmethod
#     def run_process(func,param):
#         """
#         run out of time function.
#         :param func:
#         :param param:
#         :return:
#         """
#         @timeout_decorator.timeout(RunRequestTimeOut.wait_time, timeout_exception=TimeOutRequest)
#         def process(func,param):
#             return func(param)
#         res = None
#         try:
#             res = process(func,param)
#         except TimeOutRequest:
#             RunRequestTimeOut.num_run+=1
#             print("time out %d time"%RunRequestTimeOut.num_run)
#             if RunRequestTimeOut.num_run > RunRequestTimeOut.max_run_time:
#                 res = None
#             else:
#                 res = RunRequestTimeOut.run_process(func,param)
#         except Exception as ex:
#             print ex
#             print("Unexpected error:", sys.exc_info()[0])
#             Thow
#         finally:
#             RunRequestTimeOut.num_run = 0
#             return res
#

class FileTool:
    @staticmethod
    def read_json_file(path):
        """
        read json file
        :param path:
        :return: json data
        """
        path = FileTool.__fix_path(path)
        json_data = open(path,'r').read()
        return json.loads(json_data)

    @staticmethod
    def read_text_file(i_file, encoding='utf-8'):
        """
        get list data in file
        :param i_file: filename need to be read
        :return list data
        """
        i_file = FileTool.__fix_path(i_file)
        with codecs.open(i_file, "r", "utf-8") as f:
            lines = f.read().splitlines()
        return lines

    @staticmethod
    def write_json_file(o_file, data, encoding='utf-8'):
        """
        write json file
        :param path:
        :return: json data
        """
        o_file = FileTool.__fix_path(o_file)
        with open(o_file, 'w') as out_file:
            out_file.write(data)

    @staticmethod
    def write_json_list_file(o_file, data, encoding='utf-8'):
        """
        write json file
        :param path:
        :return: json data
        """
        # o_file = FileTool.__fix_path(o_file)
        with open(o_file, 'w') as out_file:
            out_file.write('\n'.join(map(lambda x: json.dumps(x), data)))

    @staticmethod
    def write_text_file(o_file, data, encoding='utf-8'):
        """
        write data to o_file
        :param o_file: out file path
        :param data:
        :param encoding:
        """
        o_file = FileTool.__fix_path(o_file)
        with open(o_file, 'w') as out_file:
            out_file.write('\n'.join(map(lambda x: str(x), data)))

    @staticmethod
    def __fix_path(path):
        if not os.path.exists(path):
            path = "%s%s" % ("../", path)
        return path

    @staticmethod
    def read_text_csv(i_file,elim = ',', encoding='utf-8'):
        """
        get list data in file
        :param i_file: filename need to be read
        :return list data
        """
        i_file = FileTool.__fix_path(i_file)
        lines = []
        with codecs.open(i_file, "r", "utf-8") as f:
            lines = f.read().splitlines()
        lines = map(lambda x: x.split(elim), lines)
        return lines

    # def writeexcel(filename, listinfo, listtitle):
    #     """
    #     write list info into excel file, with init title
    #     :param filename: file name of excel file
    #     :param listinfo: list data need to write into excel
    #     :param listtitle: list title is respective with list data
    #     :return: None
    #     """
    #     workbook = xlsxwriter.Workbook(filename + '.xlsx')
    #     worksheet = workbook.add_worksheet()
    #     row = col = 0
    #     for ele in listtitle:
    #         worksheet.write(row, col, ele)
    #         col += 1
    #     row += 1
    #     for ele in (listinfo):
    #         col = 0
    #         for e in ele:
    #             worksheet.write(row, col, e)
    #             col += 1
    #         row += 1
    #
    #     workbook.close()

    def writeIntoCsvTemp(filename, listinfo):
        def process(data):
            str = "%s" % data[0]
            for ele in data[1:]:
                if type(ele) == type(""):
                    ele = ele.replace("\t", "  ")
                str += "\t%s" % ele
            return str

        # print cvs
        with open(filename, 'w') as out_file:
            out_file.write('\n'.join(map(lambda x: process(x), listinfo)))

    def makeCSVFromData(crawlable, crawling, listdata, title):
        csv = title.replace(",", "\t") + '\n'

        for ele in crawling:
            str = ""
            for e in ele:
                str += "'%s'\t" % e
            str += "'crawling...'"
            csv += str + '\n'

        for ele in crawlable:
            str = ""
            str += "'%s'\t'%s'" % (ele[0], ele[1])
            csv += str + '\n'

        if listdata != None:
            for ele in listdata:
                str = ""
                str += "'%s'\t'%s'" % (ele[0], ele[1])
                csv += str + '\n'

        return csv

    @staticmethod
    def writePickle(filename, data):
        pickle.dump(data, open(filename, "wb"))


    @staticmethod
    def readPickle(filename):
        return pickle.load(open(filename, "rb"))

class JsonParser:
    @staticmethod
    def parse_date(strDate="2017-10-05T05:55:32+0000"):
        strDate = strDate.replace("T"," ")
        if "+" in strDate:
            strDate = strDate[0:strDate.index("+")]
        return datetime.datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_tag(json, tag):
        if tag in json:
            return json[tag]
        else:
            print("%s not in %s" % (tag, json))
            return None

    @staticmethod
    def get_neat_tags(json, tags):
        if json == None:
            return None
        if len(tags)<=0:
            return json
        elif tags[0] in json:
            return JsonParser.get_neat_tags(json[tags[0]],tags[1:])
        else:
            print("%s not in %s" % (tags[0], json))
            return None

    @staticmethod
    def get_loop_tag(json, tag):
        if "data" in json:
            list = []
            for ele in json["data"]:
                if JsonParser.get_tag(ele,tag) != None:
                    list.append(ele[tag])
            return list
        else:
            return []

    @staticmethod
    def find_all_tag(json, tag):
        res = []
        if type(json) is list:
            for ele in json:
                res.extend(JsonParser.find_all_tag(ele,tag))
        elif type(json) is dict:
            if tag in json:
                res.append(json[tag])
            for key in json:
                res.extend(JsonParser.find_all_tag(json[key],tag))
        return res

class RandomWait:
    @staticmethod
    def wait(numSeconds, range):
        rd = random.uniform(-range, range)
        time.sleep(numSeconds,rd)

class ListTool:
    @staticmethod
    def splitList(initList, numEle):
        resultList = []
        tempList = []
        ind = 0
        for ele in initList:
            ind+=1
            tempList.append(ele)
            if ind >= numEle:
                resultList.append(tempList)
                tempList=[]
                ind =0
        if len(tempList) > 0:
            resultList.append(tempList)

        return resultList
