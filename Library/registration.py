#! /usr/bin/python3
import base64
def getSETIXML():
    import urllibRequests as ur
    data = ur.get('http://setiathome.berkeley.edu/stats/user.gz',codec='raw')
    import gzip
    stdout = open('../Data/SETIUser.xml','wb')
    stdout.write(gzip.decompress(data))
    stdout.close()
    data = ur.get('http://setiathome.berkeley.edu/stats/tables.xml',codec='raw')
    stdout = open('../Data/SETIInfo.xml','wb')
    stdout.write(data)
    stdout.close()

# This program would store all registration-related data into SETI table.
def makeDB(fileName):
    try:
        localInfo = open('../Data/SETIInfo.xml','r')
        localTime = localInfo.read().split()[4][13:-14]
    except:
        getSETIXML()
    else:
        import urllibRequests as ur
        remoteTime = ur.get('http://setiathome.berkeley.edu/stats/tables.xml').split()[4][13:-14]
        if int(localTime) < int(remoteTime):
            print('The local SETI users.xml is old, updating...')
#            getSETIXML()
    # Now it is safe to assume that the ../Data/SETIUser.xml is up to date.
    import sqlfile as sqldb
    try:
        db = sqldb.sqliteDB(fileName,'seti')
    except:
        sqldb.createSQLiteDB(fileName,['CPID','Nickname','Country'],'seti')
        db = sqldb.sqliteDB(fileName,'seti')
    print('Creating the SETI User SQLite DB...')
    # Time to parse the whole XML file...
    import xml.etree.ElementTree as ET
    tree = ET.iterparse('../Data/SETIUser.xml')
    for (event,elem) in tree:
        if elem.tag == 'user':
            cpid = elem.find('cpid').text
            uid = elem.find('id').text
            if int(uid) % 10000 == 0:
                print('Processing uid',uid)
            try:
                uname = base64.b64encode(elem.find('name').text.encode('utf-8')).decode('ascii')
            except:
                uname = base64.b64encode(b'NoName').decode('ascii')
                print(uid,cpid,elem.find('name').text)
            country = elem.find('country').text
            if not country:
                country = 'International'
            db.addItem([uid,cpid,uname,country])
            elem.clear()
    db.updateDB()
    print('SETI User DB was created successfully.')

def main():
    makeDB('../Data/SETIUser.sql')

if __name__ == '__main__':
    main()
