#!/env/python
# coding: gb2312

import os
import time
import win32com.client

#ȫ�ֱ���
valid_time = '8:30' # ����ˢ��ʱ��
eventDate = time.strftime('%Y-%m-%d') # ��������
save_path = 'd:\\'

def main():
    # ȫ�ֱ���
    nameDict = {} # ��Ա������������Ա���������
    eventList = {} # ��Ա�����嵥��������Ա������Ӧ��ˢ���б�


    # ��ʼ�����ݿ�����
    conn = win32com.client.Dispatch('ADODB.Connection')
    conn.Open('Data Source=menjin') # 'menjin' ��һ���Ѿ����õ� ϵͳDSN

    # ��ȡ���ݿ⣬������Ա����
    sql = '''
        select u.UserID, u.UserName from PubUserInfo u
        where u.UserID > '000' and u.UserID < '600' '''
    rs, success = conn.Execute(sql) 
    while not rs.EOF:
        uid = rs.Fields('UserID').Value
        name = rs.Fields('UserName').Value
        nameDict[uid] = name
        rs.MoveNext()

    # ��ȡָ��������Աˢ�������������Աˢ���嵥
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
            events.append(eventtime[:-6]) # ʱ��ԭʼ��ʽ�� 2010-11-27 13:54:59+00:00����λ����
            rs.MoveNext()
        events.reverse() # ԭʼʱ����������ǰ�棬�����Ҫȡ���������������
        eventList[uid] = events 

    # �ж�ˢ��״̬���γɿ��ڽ���
    for uid in eventList:
        events = eventList[uid]
        eventList[uid] = checkEvent(events, valid_time)

    # �����ս��д�� Excel ���
    writeExcel(nameDict, eventList)
        
def checkEvent(timeList, validTime):
    ''' ������α����
    accept_delay = 5 # �ɽ��ܵĳٵ�������
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
    #?��������ʱ����
    if timeList == []:
        timeList = ['û��ˢ����¼']
    return (timeList[0], '����ٵ�29����')

def writeExcel(nameDict, eventList):
    columns = ('���', '����', 'Ҫ����ʱ��', 'ʵ�ʿ���ʱ��', '���ڽ���')
    excel = win32com.client.Dispatch('Excel.Application')
    excel.WorkBooks.Add()
    excel.Range('B1:D1').Merge()
    excel.Range('B1:D1').Value = '����ͨ���� (' + eventDate + ')'
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
    n = {'001':'����','002':'����'}
    e = {'001':('2010-11-27 08:54:59', '�ٵ�'), 
         '002':('2010-11-27 08:24:59', '��������')}
    writeExcel(n,e)
