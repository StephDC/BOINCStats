#! /usr/bin/python3
import base64
def getSETIXML(url,projAbbr):
    import urllibRequests as ur
    data = ur.get(url+'/stats/user.gz',codec='raw')
    import gzip
    stdout = open('../Data/'+projAbbr+'User.xml','wb')
    stdout.write(gzip.decompress(data))
    stdout.close()
    data = ur.get(url+'/stats/tables.xml',codec='raw')
    stdout = open('../Data/'+projAbbr+'Info.xml','wb')
    stdout.write(data)
    stdout.close()

# This program would store all registration-related data into SETI table.
def makeDB(fileName,projAbbr,webUrl):
    try:
        localInfo = open('../Data/'+projAbbr+'Info.xml','r')
        localTime = localInfo.read().split()[4][13:-14]
    except:
        getSETIXML(webUrl,projAbbr)
    else:
        import urllibRequests as ur
        remoteTime = ur.get(webUrl+'/stats/tables.xml').split()[4][13:-14]
        if int(localTime) < int(remoteTime):
            print('The local '+projAbbr+' users.xml is old, updating...')
            getSETIXML(webUrl,projAbbr)
        print('The local '+projAbbr+' users.xml is fresh now.')
    # Now it is safe to assume that the ../Data/SETIUser.xml is up to date.
    import sqldb
    try:
        db = sqldb.sqliteDB(fileName,projAbbr.lower())
    except:
        sqldb.createSQLiteDB(fileName,['CPID','Nickname','Country','Score'],projAbbr.lower())
        db = sqldb.sqliteDB(fileName,projAbbr.lower())
    print('Creating the '+projAbbr+' User SQLite DB...')
    # Time to parse the whole XML file...
    import xml.etree.ElementTree as ET
    tree = ET.iterparse('../Data/'+projAbbr+'User.xml')
    for (event,elem) in tree:
        if elem.tag == 'user':
            cpid = elem.find('cpid').text
            uid = elem.find('id').text
            if int(uid) % 10000 == 0:
                print('Processing uid',uid)
            score = elem.find('total_credit').text
            uname = elem.find('name').text
            if not uname:
                uname = "NoName"
            uname = base64.b64encode(uname.encode('utf-8')).decode('ascii')
            country = elem.find('country').text
            if not country:
                country = 'International'
            db.addItem([uid,cpid,uname,country,score])
            db.updateDB()
            elem.clear()
    print(projAbbr+' User DB was created successfully.')

def main():
    makeDB('../Data/Users.sql','POGS','https://pogs.theskynet.org/pogs')

if __name__ == '__main__':
    main()
