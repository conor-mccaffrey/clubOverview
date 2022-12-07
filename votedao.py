import mysql.connector
from mysql.connector import cursor
import dbconfig as cfg
import sys
import traceback

###Let's get Connected###
################################################################################

class VoteDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
    
            self.host=       cfg.mysql['host']
            self.user=       cfg.mysql['user']
            self.password=   cfg.mysql['password']
            self.database=   cfg.mysql['database']


    def getcursor(self): 
        try:
                self.connection = mysql.connector.connect(
                    host=       self.host,
                    user=       self.user,
                    password=   self.password,
                    database=   self.database,
                )
                self.cursor = self.connection.cursor()
                return self.cursor
        except Exception as e:
            print('Invalid Login details for connecting. \nTry that again.')




    # Addition of a row entry to sports grounds
    def createSportGround(self, values):   
        cursor = self.getcursor()
        sql="INSERT INTO sportsground (pitchName, Capacity ) VALUES (%s,%s)"
        cursor.execute(sql, values)
        self.connection.commit()
        newid = cursor.lastrowid
        return newid
    
    # Addition of a row entry to club table
    def createClub(self, club):   
        cursor = self.getcursor()
        sql="INSERT INTO clubs (clubName, County ) VALUES (%s,%s)"
        cursor.execute(sql, club)
        self.connection.commit()
        newid = cursor.lastrowid
        return newid
     


 # throw in a vote for your favourite team
    def createVote(self, club):
       cursor = self.getcursor()
       sql="INSERT INTO clubVote (clubName, sender) values (%s,%s)"
       cursor.execute(sql, club)
       self.connection.commit()
       newid = cursor.lastrowid
       #self.closeAll()
       return newid

# and lets count them all
    def countvotes(self, clubName):
        cursor = self.getcursor()
        sql=" select count(*) as votes from clubVote where clubName LIKE %s"
        values = (clubName, )
        cursor.execute(sql, values)
        result = cursor.fetchone()
        count = result[0]
        return count


    # create vote table
    def createvoteTable(self):
            cursor = self.getcursor()
            sql="CREATE TABLE clubVote (ID int AUTO_INCREMENT NOT NULL PRIMARY KEY, clubName varchar(250), Sender varchar(250))"
            cursor.execute(sql)
            self.connection.commit()


    # create sportsground table
    def createSGTable(self):
            cursor = self.getcursor()
            sql="CREATE TABLE sportsground (ID int AUTO_INCREMENT NOT NULL PRIMARY KEY, pitchName varchar(250), Capacity int)"
            cursor.execute(sql)
            self.connection.commit()
    
    # create club table
    def createclubTable(self):
            cursor = self.getcursor()
            sql="CREATE TABLE clubs (ID int AUTO_INCREMENT NOT NULL PRIMARY KEY, clubName varchar(250), County varchar(250))"
            cursor.execute(sql)
            self.connection.commit()

    # create database
    def createDatabase(self):
            self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            )
            self.cursor = self.connection.cursor()
            sql="create database "+ self.database
            self.cursor.execute(sql)

            self.connection.commit()

    #retrieve data from club table and convert 
    def getallClubs(self):
        cursor = self.getcursor()
        sql = 'select * from clubs'
        #values = ()
        cursor.execute(sql)
        clubs = cursor.fetchall()
        returnArray = []
        #print(returnArray)
        for club in clubs:
            clubAsDict = self.convertToDictClub(club)
            returnArray.append(clubAsDict)

            print(type(returnArray))
        return returnArray

    #retrieve data from sportsground table and convert  
    def getallGrounds(self):
        cursor = self.getcursor()
        sql = 'select * from sportsground'
        #values = ()
        cursor.execute(sql)
        grounds = cursor.fetchall()
        returnArray = []
        for ground in grounds:
            groundAsDict = self.convertToDictGround(ground)
            returnArray.append(groundAsDict)
            #print(type(returnArra))

        return returnArray


    # Convert our results to a Dict
    def convertToDictClub(self, result):
        colnames = ['ID', 'clubName', 'County',]
        club = {}
        #print('fsd')
        if result:
            for i , colName in enumerate(colnames):
                value = result[i]
                club[colName] = value
              

        return club

    # Convert our results to a Dict
    def convertToDictGround(self, result):
        colnames = ['ID', 'pitchName', 'Capacity',]
        res = {}
        if result:
            for i , colName in enumerate(colnames):
                value = result[i]
                res[colName] = value
        
        return res

                
    #Find by specific ID
    def locateClub(self, ID):
        cursor = self.getcursor()
        sql = 'select * from clubs where ID = %s'
        values = [ ID ]
        cursor.execute(sql, values)
        result = cursor.fetchone()        
        return self.convertToDictClub(result)

    #Find by specific ID
    def locateGround(self, ID):
        cursor = self.getcursor()
        sql = 'select * from sportsground where ID = %s'
        values = [ ID ]
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictGround(result)

    #Update entry from clubs table
    def updateclub(self, values):
            try:
                cursor = self.getcursor()
                sql = "update clubs set clubName = %s, County = %s where ID = %s"
                cursor.execute(sql, values)
                self.connection.commit()
                rowcount = cursor.rowcount
                #print(cursor.statement)
                return rowcount
            except Exception as e:
                print(f"Hit an error {e}")
                return str(e)

    #Update entry from sportsground table
    def updatesportsground(self, values):
        try:
            cursor = self.getcursor
            sql = 'update sportsground set pitchName = %s, Capacity = %s'
            cursor.execute(sql, values)
            self.connection.commit()   
            rowcount = cursor.rowcount
                #print(cursor.statement)
            return rowcount
        except Exception as e:
            print(f"Hit an error {e}")
            return str(e)
                

        #Delete entry from clubs table
    def deleteclub(self, ID):
            cursor = self.getcursor()
            sql = 'delete from clubs where ID = %s'
            values = [ID]
            cursor.execute(sql, values)
            self.connection.commit()   

            return {}

        #Delete entry from sportsround table
    def deletesportsground(self, ID):
            cursor = self.getcursor()
            sql = 'delete from sportsground where ID = %s'
            values = [ID]
            cursor.execute(sql, values)
            self.connection.commit()   

            return {}


voteDAO = VoteDAO()





if __name__ == "__main__":
    voteDAO.createDatabase()
    voteDAO.createSGTable()
    voteDAO.createclubTable()
    voteDAO.createvoteTable()
    #print('done')
    sportsGround=("Pairc Gael na Soinnaine", "20000")
    voteDAO.createSportGround(sportsGround)
    sportsGround=("Maghera Park", "10000")
    voteDAO.createSportGround(sportsGround)
    sportsGround=("Breffni Park", "28000")
    voteDAO.createSportGround(sportsGround)
    club=("Shannon Gaels", "Cavan")
    voteDAO.createClub(club)
    club=("Maghera", "Cavan")
    voteDAO.createClub(club)
    club=("Cavan Gaels", "Cavan")
    voteDAO.createClub(club)
    club=("Courlough", "Cavan")
    voteDAO.createClub(club)
    club=("St.Kilda", "Roscommon")
    voteDAO.createClub(club)
    clubV=("St.Kilda", "Online")
    voteDAO.createVote(clubV)




    '''
    def createdatase(self):
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password   
        )
        self.cursor = self.connection.cursor()
        sql="create database "+ self.database
        self.cursor.execute(sql)

        self.connection.commit()
        self.closeAll()
'''