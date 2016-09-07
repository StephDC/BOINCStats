#! /usr/bin/env python3
import base64
import sqldb
import psvdb
import xml.etree.ElementTree as ET
import urllibRequests as UR
import time

def getNewScore(url,pid):
    req = UR.get(url+'?format=xml&userid='+pid)
    parse = ET.fromstring(req)
    score = parse.find('total_credit').text
    return score[:score.index('.')]

def main():
    newList = psvdb.psvDB('../Data/csgStats.psv')
    ts = str(int(time.time()))
    for key in newList.data.keys():
        if key != 'header':
            pid = newList.getItem(key,'pid')
            newScore = getNewScore('http://csgrid.org/csg/show_user.php',pid)
            newList.addItem([key]+newList.data[key]+[newScore])
    newList.addItem(['header']+newList.data['header']+[ts])

if __name__ == '__main__':
    main()
