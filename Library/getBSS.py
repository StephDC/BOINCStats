#! /usr/bin/python3

import urllib.request
import projectInfo
import sys
import datetime
import gzip

def readSV(fName):
    stdin=open(fName,'r')
    result=[]
    for line in stdin:
        tmp=''
        item=[]
        for c in line:
            if c=='|':
                item.append(tmp.strip())
                tmp=''
            else:
                tmp=tmp+c
        item.append(tmp.strip())
        result.append(item)
    stdin.close()
    return result

def getBSID(userID,project,initDate,finalDate):
    url = 'http://boincstats.com/en/stats/'+projectInfo.projData(project)['bsid']
    url += '/user/detail/'+str(userID)+'/lastDays'
    webRequest = urllib.request.Request(url=url,headers={'User-Agent':'Python-StephStats/1.0 (admin@hanfubk.com http://personal.psu.edu/svz5160/os/webserver/BOINC','Accept-Encoding':'gzip'})
    try:
        data = urllib.request.urlopen(webRequest)
    except urllib.error.HTTPError as e:
        print('User '+str(userID)+' failed to obtain score from BOINCStats. Reason: '+str(e.code))
        result = 'ERROR'
    else:
        dataList = gzip.decompress(data.read()).decode().split('\n')
        initScoreLine = dataList.index('<th class="right">'+initDate+'</th>')
        initScore = int(dataList[initScoreLine+13][18:-5].replace(',',''))
        finalScoreLine = dataList.index('<th class="right">'+finalDate+'</th>')
        finalScore = int(dataList[finalScoreLine+13][18:-5].replace(',',''))
        result = str(finalScore - initScore)
    return result

def main(projAbbr):
    infName = projAbbr+'/'+projAbbr+'Stats.psv'
    oufName = projAbbr+'/'+projAbbr+'Score.psv'
    nList = readSV(infName)
    projIDList = nList[3]
    initTimeStamp = str(datetime.datetime.utcfromtimestamp(int(nList[5][0])).date())
    finalTimeStamp = str(datetime.datetime.utcfromtimestamp(int(nList[-1][0])).date()-datetime.timedelta(days=0))
    bsScore = ['BOINCStats Score']
    for item in range(len(projIDList)-1):
        bsScore.append(getBSID(projIDList[item+1],projAbbr,initTimeStamp,finalTimeStamp))
    outFile = open(oufName,'w')
    for line in nList[:4]:
        tmp = ''
        for item in line:
            tmp+=(item+'|')
        outFile.write(tmp[:-1]+'\n')
    nList[-1][0]='StephStats Score'
    tmp = ''
    for item in nList[-1]:
        tmp+=(item+'|')
    outFile.write(tmp[:-1]+'\n')
    tmp = ''
    for item in bsScore:
        tmp+=(item+'|')
    outFile.write(tmp[:-1]+'\n')
    outFile.close()

if __name__ == '__main__':
    main(sys.argv[1])
