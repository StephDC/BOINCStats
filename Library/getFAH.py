#! /usr/bin/env python3

import urllibRequests
import xml.etree.ElementTree as ET
import time

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

def writeSV(fName,data):
    stdout = open(fName,'w')
    for line in data:
        firstItem = True
        for item in line:
            if not firstItem:
                stdout.write('|')
            else:
                firstItem = False
            stdout.write(item)
        stdout.write('\n')

def getUID(nName):
    data = urllibRequests.get(
        'http://folding.extremeoverclocking.com/xml/user_summary.php?un='+nName+'&t=3213')
    return ET.fromstring(data)[1].find('UserID').text

def getScore(userID,dateStr):
    data = urllibRequests.get(
        'http://folding.extremeoverclocking.com/user_summary.php?s=&u='+userID,
        codec='iso-8859-1').splitlines()
    return data[data.index('  <td>'+dateStr+'</td>')+1][20:-5].replace(',','')

def main():
    data = readSV('register.psv')
    for line in data:
        line.append(getUID(line[1]))
        time.sleep(1)
        line.append(getScore(line[2],'04.03.16'))
        print(line)
        time.sleep(1)
    writeSV('score.psv',data)

if __name__ == '__main__':
    main()