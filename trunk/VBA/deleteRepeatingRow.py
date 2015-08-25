#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''本代码实现了对指定excel表格中重复的行进行删除。
演示了通过 python 的 win32com 模块，如何处理 Excel 文档。
所演示的功能，类似于Excel中的“高级筛选”之“将筛选结果复制到指定位置”，
并且将“选择不重复的数据”选项打钩。
'''

import win32com.client

filename = 'd:\\temp\\f.xls' #待处理的 excel 文件
sheetname = 't' #待处理的 excel 文件中的表格
first_row = 2 #第一个数据行所在

def main():
    #-初始化 VBA 环境    
    excel = win32com.client.Dispatch('Excel.Application')
    excel.Workbooks.Open(filename)
    mysheet = excel.Sheets(sheetname)
    s = excel.Sheets.Add()
    resSheet = excel.Sheets(s.Name)
    last_row = mysheet.UsedRange.Rows.Count
    result_row = 1
    print('the sheet', sheetname, 'has', last_row, 'rows.')
    repeatRow = 0
    keys = []
    isRowsRepeated = []

    #- 获取行标识字段（本段运行效率最低）
    print('get the identifier of the rows.')
    for i in range(first_row, last_row + 1):
        keys.append((mysheet.Cells(i,1).Value, mysheet.Cells(i,3).Value))
        isRowsRepeated.append(0)
    
    #-将所有重复的行打上标识
    print('mark the repeat rows.')
    for i in range(0, last_row - 1):
        if isRowsRepeated[i]:continue
        key1 = keys[i]
        for j in range(i+1, last_row - 1):
            key2 = keys[j]
            if key2 == key1:
                isRowsRepeated[j] = 1
                repeatRow += 1
    
    #-拷贝不重复的行到一个新的表格中
    print('copying the non-repeat rows.', end='')
    for i in range(0, last_row - 1):
        if not isRowsRepeated[i] :
            mysheet.Rows(i + first_row).copy
            resSheet.Rows(result_row).insert
            result_row = result_row + 1
            print('.', end='')

    # 保存结果数据，关闭 Excel 文档
    print(' end.  \nFound', repeatRow, 'rows repeated.')
    excel.ActiveWorkbook.Save()
    excel.Workbooks.Close()
    excel.Quit()

if __name__ == '__main__':
    main()