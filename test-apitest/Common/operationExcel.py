'''
读取跟设置数据（Excel）
'''

import os
import xlrd
from Common import Log
from Config import ReadConfig
from xlutils.copy import copy

global path


class operationExcel:

    def __init__(self, table_name, sheet_name):
        self.logger = Log.log('operation_excel').logger
        readconfig = ReadConfig.readconfig()
        dir_path = readconfig.get_basepath("base_path")
        self.name = sheet_name
        self.path = os.path.join(dir_path, 'TestFile', table_name)  # 路径配置
        try:
            self.rwexcel = xlrd.open_workbook(self.path, encoding_override='utf-8')
            self.shelldata = self.rwexcel.sheet_by_name(self.name)
        except Exception as e:
            self.logger.error("没有用例Excel，请创建并确认有数据", e)

    # 获取表中某个shell所有的数据
    def get_all_data(self):
        try:
            data = []
            countrows = self.shelldata.nrows  # 总行数
            countcols = self.shelldata.ncols  # 总列数
            for i in range(countrows):
                rowdata = self.shelldata.row_values(i)
                if rowdata[0] != 'case_name':
                    data.append(rowdata)
            return data
        except BaseException:
            self.logger.error("Excel文件错误")
            raise xlrd.XLRDError('xlrd异常中断')

    # 获取某一行的数据
    def get_row_data(self, rowIndex):
        data = self.shelldata.row_values(rowIndex)
        return data

    # 获取某一列的内容
    def get_col_data(self, colIndex):
        str = self.shelldata.col_values(colIndex)
        return str

    # 获取某一个单元格的内容
    def get_cell_value(self, row, col):
        data = self.shelldata.cell_value(row, col)
        return data

    # 根据列名获取列号                                  #新增方法 2019/08/29
    def get_col_name_num(self, name):
        data_one_row = self.get_row_data(0)  # 获取第一行字段数据
        check = False
        col_index = 0
        for s in data_one_row:  # 遍历寻找符合名字的列的列数
            if s == name:
                check = True
                break
            else:
                col_index += 1
        if check:
            return col_index
        else:
            self.logger.error("列名-{0}不存在".format(name))
            raise xlrd.XLRDError('xlrd异常中断')

    # 获取特定列名的列数据
    def get_col_name_data(self, name):  # 新加方法 2019/8/2 陈俊安、、2019/09/29修改 陈俊安
        colIndex = self.get_col_name_num(name)
        try:
            str = self.get_col_data(colIndex)  # 返回该列数据
            return str
        except IndexError:
            self.logger.error('未找到对应列名')

    # 写入数据
    def write_value(self, row, col, value):  # 该方法仅支持xls格式
        rwexcel = xlrd.open_workbook(self.path, encoding_override='utf-8')
        sheet = self.get_sheet_index(self.name)
        wb = copy(rwexcel)
        ws = wb.get_sheet(self.name)  # 获取第sheet
        if len(str(value)) > 32767:
            value = str(value)[:32767]
        ws.write(row, col, str(value))  # 修改特定单元格信息
        wb.save(self.path)

    # 根据对应的caseid找到对应的行号                                #已修改   2018/8/2  陈俊安
    def get_caseid_row(self, caseid):
        i = 0
        str = self.get_col_name_data("caseid")
        print()
        print(str)
        for s in str:
            if s == caseid:
                return i
            else:
                i = i + 1

    # 根据对应的caseid找到对应行内容
    def get_caseid_row_data(self, caseid):
        row = self.get_caseid_row(caseid)
        data = self.get_row_data(row)
        return data

    # 获取shell表总行数
    def get_shell_nrow(self):
        countrows = self.shelldata.nrows
        return countrows

    # 根据sheet名称获取其索引值
    def get_sheet_index(self, name):
        sheet_names = self.rwexcel.sheet_names()
        check = False
        sheet_index = 0
        for sheet in sheet_names:  # 遍历寻找符合名字的列的列数
            if sheet == name:
                check = True
                break
            else:
                sheet_index += 1
        if check:
            return sheet_index
        else:
            self.logger.error("列名-{0}不存在".format(name))
            raise xlrd.XLRDError('xlrd异常中断')


    # 测试用例写入excel公共方法
    # def writer_result(self,id,test_result,response):
    #     col_num1 = self.get_col_name_num("实际结果")
    #     col_num2 = self.get_col_name_num("测试结果")
    #     row_number = int(id()[-2:])
    #
    #     try:
    #         self.write_value(row_number, col_num1, response.json())
    #     except Exception as e:
    #         self.logger.error(repr(e))
    #         self.write_value(row_number, col_num1, "写入失败：%s" % repr(e))
    #     self.write_value(row_number, col_num2, test_result)


if __name__ == '__main__':
    excel = operationExcel("flight_interface_data.xls", "login")
    print(excel.get_sheet_index("pay"))
