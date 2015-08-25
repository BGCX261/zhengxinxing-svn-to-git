#!/env/python
# coding: gb2312

import os
import time
import win32com.client

#全局变量
valid_time = '8:30' # 上午刷卡时间
eventDate = time.strftime('%Y-%m-%d') # 考勤日期
save_path = 'd:\\'

def main():
    # 全局变量
    nameDict = {} # 人员名单，包括人员编号与姓名
    eventList = {} # 人员考勤清单，包括人员编号与对应的刷卡列表


    # 初始化数据库连接
    conn = win32com.client.Dispatch('ADODB.Connection')
    conn.Open('Data Source=menjin') # 'menjin' 是一个已经建好的 系统DSN

    # 读取数据库，建立人员名单
    sql = '''
        select u.UserID, u.UserName from PubUserInfo u
        where u.UserID > '000' and u.UserID < '600' '''
    rs, success = conn.Execute(sql) 
    while not rs.EOF:
        uid = rs.Fields('UserID').Value
        name = rs.Fields('UserName').Value
        nameDict[uid] = name
        rs.MoveNext()

    # 读取指定日期人员刷卡情况，建立人员刷卡清单
    #? for uid in ['001',]:
    for uid in nameDict:
        today = 'DATEADD(dd, DATEDIFF(dd,0,getdate()), 0)'
        sql = '''
            select v.EventTime from PubValidCardEvent as v
            where v.UserID='%s'
            and v.EventTime>%s
            ''' % (uid, today)
        rs, success = conn.Execute(sql)
        events = []
        while not rs.EOF :
            eventtime = str(rs.Fields('EventTime').Value)
            events.append(eventtime[:-6]) # 时间原始格式是 2010-11-27 13:54:59+00:00，后几位无用
            rs.MoveNext()
        events.reverse() # 原始时间最后的在最前面，因此需要取反，方便后续处理
        eventList[uid] = events 

    # 判断刷卡状态，形成考勤结论
    for uid in eventList:
        events = eventList[uid]
        eventList[uid] = checkEvent(events, valid_time)

    # 将最终结果写入 Excel 表格
    writeExcel(nameDict, eventList)
        
def checkEvent(timeList, validTime):
    ''' 下面是伪代码
    accept_delay = 5 # 可接受的迟到分钟数
    result = 'delay'

    if timeList == []:
        result = 'no record'
    else: 
        for t in timeList:
            temp = validTime - t
            if -accept_delay < temp < 30minutes:
                result = 'OK'
            else:
                continue
                
    if result == 'delay':
        time = getEarlestTime(timeList) - validTime
        result = 'delay ' + time + ' minutes'
        
    return result
    '''
    #?下面是临时代码
    if timeList == []:
        timeList = ['没有刷卡记录']
    return (timeList[0], '上午迟到29分钟')

def writeExcel(nameDict, eventList):
    columns = ('编号', '姓名', '要求考勤时间', '实际考勤时间', '考勤结论')
    excel = win32com.client.Dispatch('Excel.Application')
    excel.WorkBooks.Add()
    excel.Range('B1:D1').Merge()
    excel.Range('B1:D1').Value = '考勤通报表 (' + eventDate + ')'
    excel.Range("A2:E2").Value = columns
    
    i = 3
    for uid in nameDict:
        excel.Cells(i, 1).Value = uid
        excel.Cells(i, 2).Value = nameDict[uid]
        excel.Cells(i, 3).Value = '08:30'
        excel.Cells(i, 4).Value = eventList[uid][0]
        excel.Cells(i, 5).Value = eventList[uid][1]
        i += 1

    excel.Columns('A:E').AutoFit()
    excel.ActiveWorkbook.SaveAs( _getFileName())
    excel.WorkBooks.Close()
    del excel

def _getFileName():
    '''return file name like 2010-11-28(1).xls with full path'''
    filename = eventDate + '.xls'
    
    while os.path.exists(save_path + filename):
        if '(' not in filename:
            number = '1'
        else:
            number = filename.split('(')[1].split(')')[0]
            number = str(int(number) + 1)
        filename =  eventDate + '(' + number + ')' + '.xls'

    return save_path + filename


    

if __name__ == '__main__':
    n = {'001':'张三','002':'李四'}
    e = {'001':('2010-11-27 08:54:59', '迟到'), 
         '002':('2010-11-27 08:24:59', '正常考勤')}
    writeExcel(n,e)
