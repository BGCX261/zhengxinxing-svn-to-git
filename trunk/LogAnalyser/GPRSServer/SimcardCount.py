#!/usr/bin/env python
##############################################################################
#Description: parse the login frame of all the GK110-G from logs of GPRS-P
##############################################################################
# release: v1.1
# author: swjr@263.net
__revision__ = '$id$'
__version__ = '1.1'


import sys, os, re, string

##
# a leading function, manages the files related I/O
##
def framesCounter(pathLog, pathOutput):
    postfix = '.log$'
    files = fileChooser(pathLog, postfix)
    totalLogins = {}
    
    for file in files :
        print '%s ' % file.split('\\')[-1] , # 只显示文件名，不显示路径
        
        #=- the main step is here :-)
        log_date, log_hour, logins = fileParser(file)
        print '.',
        
        #=- now print the parsed result
        file = '%s\\%s.txt' % ( pathOutput, file.split('\\')[-1] )
        file = open(file, 'w')
        file.write('%s %s点\n' % (log_date, log_hour) )
        writeOutput(file, logins)

        #=- get the total result
        for sim_card in logins :
            if sim_card in totalLogins :
                totalLogins[sim_card] += logins[sim_card]
            else :
                totalLogins[sim_card] = logins[sim_card]
        print '. %s' % file.name
    
    #=- print the total result 
    out = [ '=================================']
    out.append( '%d个文件的统计数据总结如下：' % len(files) )
    out.append( '=================================')
    out.append( '       SIM卡号    次数' )
    for sim in totalLogins :
        out.append( '    %s   %d' % ( sim, len( totalLogins[sim] ) ) )
    
    fileTotal = '总结.txt'
    file = open( '%s\\%s' % (pathOutput, fileTotal), 'w')
    file.writelines('\n'.join(out))
    print 'write %(fileTotal)s ok' % locals()
            
    return files
    
##
# main function for parsing one file, return the parsed result, format: 
# { '13567283226':['19:00:10', '19:00:11'], 
#   '13567283227':['19:00:13', '19:22:11'], ... }
# 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
# 31 33 37 35 37 39 38 33 37 31 35 00 00 00 00 00 00 00 00 00 00 00
##
def fileParser(fileName):
    counter = 0
    file = open(fileName)
    lines = file.readlines()
    print '.', # for easy user interface :-)
    
    #=- hold the date and the time of the log file
    log_date = lines[1][1:12]
    log_time = lines[1][12:14]
    
    #=- get all the login lines
    # login = '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 31 33 37 35 37 39 38 33 37 31 35 00 00 00 00 00 00 00 00 00 00 00'
    login = '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 31 33 3[0-9] 3[0-9] 3[0-9] 3[0-9] 3[0-9] 3[0-9] 3[0-9] 3[0-9] 3[0-9] 00 00 00 00 00 00 00 00 00 00 00'
    loginPattern = re.compile(login, re.IGNORECASE)
    lines = filter(loginPattern.search, lines)
    
    #=- format the login lines, gets ['13567283226 19:00:10', ... ]
    lines = map(formatLine, lines)

    return ( log_date, log_time, summarize(lines) )

##
# a map function for format from
# (2004-09-08 16:00:14)Recv (1):00 00 00 89 00 00 00 05 00 00 02 7f 94 3e 7e 80 df 0d 00 53 35 30 31 30 30 35 37 31 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 31 33 37 35 37 39 38 33 38 31 32 00 00 00 00 00 00 00 00 00 00 00 34 51 54 6d 2e 38 30 6c 4e 68 71 66 52 6d 73 4e 69 34 39 37 2e 55 45 36 36 35 77 30 2c 56 2c 2c 36 55 43 50 51 73 48 63 47 4c 42 76 64 58 31 4c 79 56 58 68 55 00 00 00 00 00 00 00 00 # to '13567283226 17:59:56'
##
def formatLine(line):
    l = line.split(')')
    res_time = l[0][12:]
    li = l[2][163:164+31];
    res_number = convertMobileNumber(li) 
    return '%s %s' % (res_number, res_time)

##
# a filter function for checking the length of the line
##    
def checkLength(line):
    login = '(2004-08-18 17:59:56)Recv (177):7e eb 10 11 01 01 0f 31 33 35 36 37 32 38 33 31 30 33 20 20 20 20 7e '
    max = len(login)+1
    min = max - 2
    lineLength = len(line)
    if lineLength > max or lineLength < min :
        return 0
    return 1

##
# '31 33 35 36 37 32 38 33 31 30 33' ---> '13567283103'
##
def convertMobileNumber(raw):
    numbers = raw.strip().split(' ') # use strip to get rid of the leading or trailing blankspace
    convertN = lambda p: p[1]
    numbers = map(convertN, numbers)
    return ''.join(numbers)

##
# eat ['13567283226 19:00:10', ... ], 
# output { '13567283226':['19:00:10', '19:20:11'], ... }
##
def summarize(paramLines):
    res = {}
    for l in paramLines :
        sim_card = l[:11]
        login_time = l[12:]
        
        if sim_card in res :
            res[sim_card] += [login_time]
        else :
            res[sim_card] = [login_time]
        
    return res

##
# calculate the interval in two time-stamp: '19:23:34' - '19:34:21'
##
def subTime(X,Y):
    x = int(X[3:5])*60 + int(X[6:8])
    y = int(Y[3:5])*60 + int(Y[6:8])
    return x-y
    
##
# format the result and write the output files
##
def writeOutput(file, logins):
        formatOut = []
        count = 0
        for s in logins :
            count += len(logins[s])
            
        formatOut.append( '===================================================')
        formatOut.append(  '本时间段内共收到%d个 车台发到系统的短信，共有%d车次' % ( len(logins), count ) )
        formatOut.append(  '详细重新登陆结果统计如下：' )
        formatOut.append(  '===================================================' )
        formatOut.append(  '    SIM卡号    收到短信数' )
        for sim_card in logins :
            formatOut.append(  '    %s   %d' % ( sim_card, len(logins[sim_card]) ) )
        formatOut.append(  '=================================' )
        formatOut.append(  '每辆车详细登陆时间统计如下：' )
        formatOut.append(  '=================================' )
        for sim_card in logins :
            formatOut.append(  '    %s   时间间隔   （共%d次）' % ( sim_card, len(logins[sim_card]) ) )
            last_time = ''
            for login_time in logins[sim_card] :
                if last_time == '' :
                    last_time = login_time
                interval = subTime(login_time, last_time)
                last_time = login_time
                formatOut.append(  '        %s  %d' % (login_time, interval) )
            formatOut.append(  '----------------------------------' )
        
        file.writelines( '\n'.join(formatOut) )
        return
        
#---------------------------------------------------------
# reusable functions are here
#---------------------------------------------------------
def fileChooser(path, mark):
    ''' search files in path that the file name has some mark '''
    files = os.listdir(path)
    s = re.compile(mark, re.IGNORECASE)
    files = filter(s.search, files)
    toFullName = lambda f: path + '\\' + f
    return map(toFullName, files)

def getConfig(configFileName):
    ''' read config file, get the values of each items, and return them as a dictionary '''
    file = open(configFileName)
    configs = file.readlines()
    configs = map(__strip, configs)
    configs = filter(__checkValue, configs) 
    result = {}
    for config in configs :
        result[ config.split('=')[0] ] = config.split('=')[1]
    return result

def __strip(line):
    ''' a mapping function '''
    return line.strip()
    
def __checkValue(l):
    ''' a filtering function that checks if the line begins with # '''
    if  l == '' or l[0] == '#':
        return 0
    return 1

#---------------------------------------------------------
# the main function
#---------------------------------------------------------
def main():
    configFile = 'FramesCounter.conf'
    defaultPath = 'c:\\temp'
    if not os.path.isfile(configFile) :
        print '无法找到配置文件: %(configFile)' % locals()
        print 'quit'
        return
    
    config = getConfig(configFile)
    logPath = 'GPRS_log_path'
    outputPath = 'output_path'
    if logPath not in config :
        config[logPath] = defaultPath
    if outputPath not in config :
        config[outputPath] = defaultPath
    
    declaration = """.本程序读取GPRS前置机日志，用于分析车载台重复登陆前置机现象，
分析结果包括某时段下各个车载台登陆详细情况。
程序运行前请先修改配置文件%(configFile)s，以指定日志文件所在位置
.""" % locals()
    print declaration
    print 'process log files in %s' % config[logPath]
    print 'output to %s' % config[outputPath]
    framesCounter(config[logPath], config[outputPath])
    
if __name__=='__main__':
    main()
    
""".
    change logs
    2004.08.21 v1.1
    ·优化用户界面
    ·convertMobileNumber里去掉__isNull()函数，用strip()代替实现头尾空格的删除
    ·添加配置文件功能（函数getConfig()），将输入输出目录放入配置文件
    
    2004.08.20 v1.0
    ·实现了基本功能，从一个目录里面读取GPRS前置机日志，输出每个日志文件
     的登陆帧分析结果
    ·界面比较粗糙，绝大部分参数都是硬编码，缺少输入输出参数
."""
