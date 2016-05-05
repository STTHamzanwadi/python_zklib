'''
Created on 3 Mei 2016

@author: ewien
'''
import MySQLdb
import logging

class Synchronizer():
    '''
    class to insert attendance data to database
    '''
    ip = "192.168.20.3"
    dbuser = "att"
    dbpass = "200lembaratt"
    schema = "attendance" 
    logFile = "synclog.txt"
    
    
    def __init__(self):
        '''
        Constructor
        '''
        logging.basicConfig(filename=Synchronizer.logFile,level=logging.DEBUG)
        self.db = MySQLdb.connect(Synchronizer.ip,Synchronizer.dbuser,Synchronizer.dbpass,Synchronizer.schema)
        def userLastScanTime(self):
            sql = """select max(scantime) from attrecords"""
            c = self.db.cursor()
            try:
                c.execute(sql)
                result = c.fetchall()
                if (result):
                    row = result [0]
                    return row[0]
                else:
                    return None
                
            except MySQLdb.Error as e:
                print e
                logging.error(str(e))
            finally:
                c.close()
        self.maxscantime = userLastScanTime(self)
        self.databaru = 0
        #print "max scan time : %s" % (self.maxscantime) 
        logging.info(" Scan terakhir sebelum sync :"+ str(self.maxscantime))
    def insert(self, attendanceRecord):
        
        uid = attendanceRecord[0]
        scantime = attendanceRecord[2]
        b = True
        if (self.maxscantime != None):
            if (self.maxscantime >= scantime):
                b = False
        
        if (b):
            self.databaru += 1
            print "uid scan time : %s %s" % (uid,scantime)    
            sql = """INSERT INTO attrecords(uid,scantime)
                VALUES (%s, %s)"""
            
            c = self.db.cursor()
            
            try:
                c.execute(sql,(uid,scantime))
                self.db.commit() 
                
            except MySQLdb.Error as e:
                #c.rollback()
                print e
    
            finally: 
                c.close()    
            
    
   
        
        