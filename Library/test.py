import base64
import sqldb
import psvdb
import xml.etree.ElementTree as ET
def main():
    regList = psvdb.psvDB('../Data/registration.psv')
    newList = psvdb.psvDB('../Data/csgStats.psv')
    db = sqldb.sqliteDB('../Data/Users.sql','csg')
    ts = ET.parse('../Data/CSGInfo.xml')
    notFound = []
    nextID = 0
    for key in regList.data.keys():
        fName = key
        bName = regList.data[key][0]
        try:
            pid = db.searchItem('nickname',base64.b64encode(bName.encode('utf-8')).decode('ascii'))
        except:
            notFound.append([fName,bName])
        else:
            cpid = db.getItem(pid,'cpid')
            setiID = str(nextID)
            nextID += 1
            score = db.getItem(pid,'score')
            score = score[:score.index('.')]
            newList.addItem([setiID,cpid,fName,bName,pid,score])
    newList.addItem(['header']+newList.data['header']+[ts.find('update_time').text])
    print('The following users were not found:')
    for item in notFound:
        print(item[0],item[1])

if __name__ == '__main__':
    main()
