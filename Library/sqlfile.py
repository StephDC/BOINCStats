#! /usr/bin/python3
class sqliteDBError(Exception):
    def __init__(self,e):
        self.message = e
    def __repr__(self):
        return 'SQLite DB Exception: '+self.message

# This is the file that would replace the old-fashioned PSV DB with the new SQLite database.
# A few security issues exist and might cause serious data destruction.
# The following input is not filtered: dbTable, item, key. Please filter accordingly.
class sqliteDB():
    def __init__(self,dbFile,dbTable='main'):
        self.headData = []
        self.tailData = []
        try:
            self.db = open(dbFile,'r')
        except:
            raise sqliteDBError('no such file - '+dbFile)
        self.table = dbTable
        rLine = self.db.readline()
        self.headData.append(rLine)
        while bool(rLine):
            if rLine[:2] == '--':
                headerList = rLine[2:].split(',')
                if headerList[0] == self.table:
                    break
            rLine = self.db.readline()
            self.headData.append(rLine)
        if not bool(rLine):
            raise sqliteDBError('no such table - '+dbTable)
        else:
            self.header = headerList[1:]
            self.data = []
            while bool(rLine):
                rLine = self.db.readline()
                self.data.append(rLine)
                if rLine[:2]=='--':
                    break
            self.tailData.append(self.data.pop())
            while bool(rLine):
                rLine = self.db.readline()
                self.tailData.append(rLine)
            self.db.close()
            self.db = dbFile
        if self.data[-1].strip() == 'COMMIT;':
            self.data = self.data[:-1]
            self.tailData.append('COMMIT;')

    def __str__(self):
        result = ''
        for item in self.headData:
            result += item
        for item in self.data:
            result += item
        for item in self.tailData:
            result += item
        return result

    def __repr__(self):
        self.__str__()

    def hasItem(self,item):
        raise NotImplementedError('This file is write-only.')

    def getItem(self,item,key):
        raise NotImplementedError('This file is write-only.')

    def searchItem(self,key,val):
        raise NotImplementedError('This file is write-only.')

    # This would add a new item to the database if the "header" was not used.
    # If the "header" was already used, this would update the "header" with new data.
    def addItem(self,item):
        #tmp = item[1:]
        # If we do not have the item - Add it.
        #if not self.hasItem(item[0]):
        self.data.append('INSERT INTO "'+self.table+'" VALUES ('+str(item)[1:-1]+');\n')
        #else:
        #    for key in range(len(tmp)):
        #        self.data.execute('update '+self.table+' set '+self.header[key+1]+' = "'+str(tmp[key])+'" where header = "'+item[0]+'"')
        #self.db.commit()

    def remItem(self,item):
        raise NotImplementedError('This function is not yet implemented.')
        #if not self.hasItem(item):
        #    raise sqliteDBError('item not found - '+item)
        #result = [item]
        #for key in self.header[1:]:
        #    result.append(self.getItem(item,key))
        #self.data.execute('delete from '+self.table+' where header = "'+item+'"')
        #self.db.commit()
        #return result

    def updateDB(self):
        dbFile = open(self.db,'w')
        for item in self.headData:
            dbFile.write(item)
        for item in self.data:
            dbFile.write(item)
        for item in self.tailData:
            dbFile.write(item)
        dbFile.close()

# Input: fileName - The file name of the new SQLite file
#        columnList - The list of every columns except "header" column
#        tableName - The name of the table in the SQLite file, default "main"
# Output: The corresponding SQLite file with the table that contains the header row only.
def createSQLiteDB(fileName,columnList,tableName = 'main'):
    db = open(fileName,'w')
    db.write('BEGIN TRANSACTION;\n')
    db.write('--'+tableName)
    for item in columnList:
        db.write(','+item)
    db.write('\nCREATE TABLE '+tableName+' (header, '+str(columnList)[1:-1].replace("'",'').replace('"','')+');\n')
    db.write('INSERT INTO '+tableName+' VALUES (\'header\', '+str(columnList)[1:-1]+');\n')
    db.write('COMMIT;')
    db.close()

# Input: fileName - The file name of the PSV file need to be imported
# Output: The corresponding SQLite file with .psv replaced by .sql.
# Notice: The "header" row is required.
def importPSVDB(fileName):
    import psvdb
    db = psvdb.psvDB(fileName)
    columnList = db.data['header']
    createSQLiteDB(fileName[:-3]+'sql',columnList)
    newDB = sqliteDB(fileName[:-3]+'sql')
    for key in db.data.keys():
        if key != 'header':
            newDB.addItem([key]+db.data[key])

# This process is used to protect the CGI access from the outside,
# as well as Command-line direct access.
def main():
    print('Content-Type:text/html charset:utf-8\nLocation:http://bbs.psucssa.org/cgi-bin/webAccess/\n\n')

if __name__ == '__main__':
    main()
