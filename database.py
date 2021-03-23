import sqlite3
import datetime

class Database:
    def __init__(self, databaseName: str):
        self.database = sqlite3.connect(databaseName, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cursor = self.db.cursor()

    def createTable(self, tableName: str) -> None:
        '''Creates a new table in the database'''
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS {}(TIME TIMESTAMP, USERNAME TEXT,
        USERID INT PRIMARY KEY)
        '''.format(tableName)
        self.database.commit()

    def insertEntry(self, tableName: str, username: str, userid: int) -> int:
        '''Inserts a new entry into the database'''
        try:
            currentTime = datetime.datetime.now()
            self.cursor.execute('''INSERT INTO {}(TIME, USERNAME, USERID)
            VALUES(?, ?, ?)'''.format(tableName), (currentTime, username, userid))
            self.database.commit()
            return 0
            
        except sqlite3.IntegrityError: #Return 1 if entry already in database
            return 1

    def removeEntry(self, tableName: str, userid: int) -> None:
        '''Removes an entry from the table'''
        self.cursor.execute('''DELETE FROM {} WHERE USERID=?'''.format(tableName), (userid,))
        self.database.commit()

    def getUser(self, tableName: str, userid: int) -> tuple:
        '''Gets a specific user from the table'''
        self.cursor.execute('''SELECT * FROM {} WHERE USERID=?'''.format(tableName), (userid,))
        self.database.commit()
        return self.cursor.fetchone()

    def getData(self, tableName: str) -> list:
        '''Gets all data from the table'''
        self.cursor.execute('''SELECT * FROM {}'''.format(tableName))
        return self.cursor.fetchall()

    def deleteTable(self, tableName: str) -> None:
        '''Drops the specified table from the database'''
        self.cursor.execute('''DROP TABLE {}'''.format(tableName))
        self.database.commit()

    def closeConnection(self):
        '''Closes the connection to the database'''
        self.database.commit()
        self.database.close()